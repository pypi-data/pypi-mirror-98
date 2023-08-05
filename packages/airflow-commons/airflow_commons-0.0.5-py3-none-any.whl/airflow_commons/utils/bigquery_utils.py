from google.cloud import bigquery
from datetime import datetime

from airflow_commons.logger import LOGGER
from airflow_commons.sql_resources import (
    GET_COLUMN_NAMES_SQL_FILE,
    GET_TABLE_NAMES_SQL_FILE,
    GET_OBJECT_FIELDS_SQL_FILE,
)
from airflow_commons.utils.file_utils import read_sql
from airflow_commons.glossary import COMMA


MEGABYTES_BILLED_DENOMINATOR = 2 ** 20
AVAILABLE_COLUMN_NAMES = ["column_name", "field_path", "table_name"]
DEFAULT_TIMEOUT = 60
DEFAULT_LOCATION = "US"


def connect(service_account_file: str):
    """
    Connects to Bigquery client with given service account file.

    :param service_account_file: relative location of service account json
    :return: a Client object instance required for API requests
    """
    return bigquery.Client.from_service_account_json(service_account_file)


def get_table_ref(client: bigquery.Client, dataset_id: str, table_id: str):
    """
    Returns table ref to requested table.

    :param client: Client needed for API request
    :param dataset_id: id of dataset
    :param table_id: id of table to be referred
    :return: a pointer to requested table
    """
    return client.get_dataset(dataset_id).table(table_id)


def get_dataset_ref(client: bigquery.Client, dataset_id: str):
    """
    Returns dataset ref to requested dataset.

    :param client: Client needed for API request
    :param dataset_id: id of dataset
    :return: a pointer to requested dataset
    """
    return client.get_dataset(dataset_id)


def get_table_time_partitioning_info(
    client: bigquery.Client, dataset_id: str, table_id: str
):
    """
    Returns time partitioning object of requested table.

    :param client: Client needed for API request
    :param dataset_id: id of dataset
    :param table_id: id of table
    :return: table's time partitioning info
    """
    table_ref = get_table_ref(client, dataset_id, table_id)
    return client.get_table(table_ref).time_partitioning


def query(
    client: bigquery.Client,
    job_config: bigquery.QueryJobConfig,
    sql: str,
    timeout: int,
    location: str,
):
    """
    Runs a query with given job configs, and returns job result.

    :param client: Client needed for API request
    :param job_config: query configurations, settings like destination table should be given here
    :param sql: sql query
    :param timeout: timeout configuration
    :param location: location
    :return: job result
    """
    timer_start = datetime.now()
    LOGGER("SQL TO RUN: ## " + sql + " ##")
    query_job = client.query(
        sql, location=location, timeout=timeout, job_config=job_config
    )
    result = query_job.result()
    timer_end = datetime.now()
    if query_job.state == "DONE":
        LOGGER(
            (
                "Query Job ID:",
                query_job.job_id,
                "Elapsed Time:",
                round((timer_end - timer_start).total_seconds()),
                "Total MBytes Billed:",
                query_job.total_bytes_billed / MEGABYTES_BILLED_DENOMINATOR,
                "Number of Rows Affected:",
                query_job.num_dml_affected_rows,
            )
        )
        return result
    else:
        LOGGER(
            (
                "Query Job ID:",
                query_job.job_id,
                "Elapsed Time:",
                round((timer_end - timer_start).total_seconds()),
            ),
            level=1,
        )
        raise Exception("Job is not Done.")


def query_information_schema(
    client: bigquery.Client,
    requested_column_name: str,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
    **kwargs
):
    """

    :param client: Client needed for API request
    :param requested_column_name: name of the column requested from information schema, can take values column_name,
    table_name, and field_path
    :param timeout: query timeout parameter, equals to 60 seconds on default
    :param location: query location parameter, equals to US on default
    :param kwargs:
    :return: requested field as a list
    """
    if requested_column_name == "column_name":
        sql = read_sql(GET_COLUMN_NAMES_SQL_FILE, **kwargs)
    elif requested_column_name == "table_name":
        sql = read_sql(GET_TABLE_NAMES_SQL_FILE, **kwargs)
    elif requested_column_name == "field_path":
        sql = read_sql(GET_OBJECT_FIELDS_SQL_FILE, **kwargs)
    else:
        raise ValueError(
            "Invalid requested_column_name:{}. Acceptable column names are ".format(
                requested_column_name
            )
            + COMMA.join(i for i in AVAILABLE_COLUMN_NAMES)
        )
    df_columns = select(client, sql, location=location, timeout=timeout)
    return df_columns[requested_column_name].to_list()


def select(client: bigquery.Client, sql: str, timeout: int, location: str):
    """
    Runs a select query and returns results as dataframe

    :param client: Client needed for API request
    :param sql: query sql
    :param timeout: job timeout parameter
    :param location: job location parameter
    :return: a dataframe of query result
    """
    job_config = bigquery.QueryJobConfig()
    return query(
        client=client,
        job_config=job_config,
        sql=sql,
        timeout=timeout,
        location=location,
    ).to_dataframe()


def single_value_select(
    client: bigquery.Client,
    sql: str,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a single value returning query and returns the requested key from query results

    :param client: Client needed for API request
    :param sql: query sql
    :param timeout: job timeout parameter
    :param location: job location parameter
    :return: requested value on first row
    """
    job_config = bigquery.QueryJobConfig()
    result = query(
        client=client,
        job_config=job_config,
        sql=sql,
        timeout=timeout,
        location=location,
    )
    return [i for i in result][0].values()[0]


def get_time_partition_field(client: bigquery.Client, dataset_id: str, table_id: str):
    """
    Makes an API call to get time partitioning of a table, then gets time partitioning column name from response

    :param client: Client needed for API request
    :param dataset_id: dataset id
    :param table_id: table id
    :return:
    """
    return get_table_time_partitioning_info(client, dataset_id, table_id).field
