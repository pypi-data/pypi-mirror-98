from google.cloud import bigquery

from airflow_commons.glossary import COMMA
from airflow_commons.logger import LOGGER
from airflow_commons.sql_resources.bigquery import (
    DEDUPLICATION_GET_OLDEST_PARTITION_FIELD_SQL_FILE,
    ARCHIVE_SOURCE_STATEMENT_FILE,
    ARCHIVE_DELETE_WHERE_STATEMENT_FILE,
)
from airflow_commons.utils.bigquery.bigquery_utils import (
    DEFAULT_TIMEOUT,
    DEFAULT_LOCATION,
    DEFAULT_RETURN_TYPE,
    connect,
    get_time_partition_field,
    single_value_select,
    query,
    select,
    query_information_schema,
    get_table_ref,
)
from airflow_commons.utils.file_utils import read_sql
from airflow_commons.utils.bigquery.sql_utils import (
    get_deduplication_source_statement,
    get_merge_sql,
    get_delete_sql,
    get_deduplication_additional_merge_conditions,
)
from airflow_commons.utils.time_utils import get_buffered_timestamp

ARCHIVE_MODES = ["INSERT", "UPSERT"]
WRITE_DISPOSITIONS = ["WRITE_APPEND", "WRITE_TRUNCATE", "WRITE_EMPTY"]
DEFAULT_PRIMARY_KEYS = ["id"]
ARCHIVE_DEFAULT_PRIMARY_KEYS = ["id", "last_updated_at", "processed_at"]
DEFAULT_TIME_COLUMNS = ["last_updated_at", "processed_at"]


def deduplicate(
    service_account_file: str,
    start_date: str,
    end_date: str,
    project_id: str,
    source_dataset: str,
    source_table: str,
    target_dataset: str,
    target_table: str,
    oldest_allowable_target_partition: str,
    primary_keys=None,
    time_columns=None,
    allow_partition_pruning: bool = True,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a merge query to deduplicate rows in historic table, and write to target snapshot table

    :param service_account_file: relative location of service account json
    :param start_date: deduplication interval start
    :param end_date: deduplication interval end
    :param project_id: Bigquery project id
    :param source_dataset: source dataset id
    :param source_table: source table id
    :param target_dataset: target dataset id
    :param target_table: target table id
    :param oldest_allowable_target_partition: oldest value of time partition column value to be added to target table, aims to keep partition count below limit
    :param primary_keys: primary key columns of the source and target tables
    :param time_columns: time columns list to order rows
    :param allow_partition_pruning: partition pruning allow parameter, if true prunes target table's partitions to limit query size
    :param timeout: query timeout duration parameter
    :param location: query location parameter
    :return:
    """
    client = connect(service_account_file)
    if primary_keys is None:
        primary_keys = DEFAULT_PRIMARY_KEYS
    if time_columns is None:
        time_columns = DEFAULT_TIME_COLUMNS
    buffered_start_date = get_buffered_timestamp(start_date)
    source_partition_field = get_time_partition_field(
        client, source_dataset, source_table
    )
    partition_pruning_params = dict()
    additional_merge_conditions = None
    partition_pruning_params["target_partition_field"] = get_time_partition_field(
        client, target_dataset, target_table
    )
    if allow_partition_pruning:
        partition_pruning_params["oldest_target_partition"] = single_value_select(
            client=client,
            sql=read_sql(
                sql_file=DEDUPLICATION_GET_OLDEST_PARTITION_FIELD_SQL_FILE,
                project_id=project_id,
                source_dataset=source_dataset,
                source_table=source_table,
                target_partition_field=partition_pruning_params[
                    "target_partition_field"
                ],
                source_partition_field=source_partition_field,
                start_date=buffered_start_date,
                end_date=end_date,
                oldest_allowable_target_partition=oldest_allowable_target_partition,
            ),
        )
        if partition_pruning_params["oldest_target_partition"] is None:
            LOGGER(
                "There is no data: - {project_id}.{source_dataset}.{source_table} - between [{start_date} - {end_date}] .".format(
                    project_id=project_id,
                    source_dataset=source_dataset,
                    source_table=source_table,
                    start_date=buffered_start_date,
                    end_date=end_date,
                )
            )
            return None
        additional_merge_conditions = get_deduplication_additional_merge_conditions(
            partition_pruning_params=partition_pruning_params
        )
    source_statement = get_deduplication_source_statement(
        start_date=buffered_start_date,
        end_date=end_date,
        project_id=project_id,
        source_dataset=source_dataset,
        source_table=source_table,
        source_partition_field=source_partition_field,
        primary_keys=primary_keys,
        time_columns=time_columns,
        oldest_allowable_target_partition=oldest_allowable_target_partition,
        allow_partition_pruning=allow_partition_pruning,
        partition_pruning_params=partition_pruning_params,
    )
    sql = get_merge_sql(
        client=client,
        project_id=project_id,
        target_dataset=target_dataset,
        target_table=target_table,
        source_statement=source_statement,
        primary_keys=primary_keys,
        mode="UPSERT",
        additional_merge_conditions=additional_merge_conditions,
    )
    return query(
        client=client,
        job_config=bigquery.QueryJobConfig(),
        sql=sql,
        timeout=timeout,
        location=location,
    )


def upsert(
    service_account_file: str,
    source_statement_file: str,
    project_id: str,
    target_dataset: str,
    target_table: str,
    source_statement_params: dict = None,
    primary_keys=None,
    additional_merge_conditions: str = None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a merge query to upsert target table, with given source statement, merge conditions, and primary keys

    :param service_account_file: relative location of service account json
    :param source_statement_file: relative location of source statement file
    :param project_id: Bigquery project id
    :param target_dataset: targeted dataset id
    :param target_table: targeted table id
    :param source_statement_params: parameters of source statement
    :param primary_keys: target table's primary key list
    :param additional_merge_conditions: additional user specified merge conditions as string
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return:
    """
    client = connect(service_account_file)
    if source_statement_params is None:
        source_statement_params = dict()
    if primary_keys is None:
        primary_keys = DEFAULT_PRIMARY_KEYS
    source_statement = read_sql(
        sql_file=source_statement_file, **source_statement_params
    )
    sql = get_merge_sql(
        client=client,
        project_id=project_id,
        target_dataset=target_dataset,
        target_table=target_table,
        source_statement=source_statement,
        primary_keys=primary_keys,
        mode="UPSERT",
        additional_merge_conditions=additional_merge_conditions,
    )
    return query(
        client=client,
        job_config=bigquery.QueryJobConfig(),
        sql=sql,
        timeout=timeout,
        location=location,
    )


def insert(
    service_account_file: str,
    source_statement_file: str,
    project_id: str,
    target_dataset: str,
    target_table: str,
    source_statement_params: dict = None,
    primary_keys=None,
    additional_merge_conditions: str = None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a merge query to insert non-existing rows to target table, with given source statement, merge conditions, and primary keys

    :param service_account_file: relative location of service account json
    :param source_statement_file: relative location of source statement file
    :param project_id: Bigquery project id
    :param target_dataset: targeted dataset id
    :param target_table: targeted table id
    :param source_statement_params: parameters of source statement
    :param additional_merge_conditions: additional user specified merge conditions as string
    :param primary_keys: target table's primary key list
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return:
    """
    client = connect(service_account_file)
    if source_statement_params is None:
        source_statement_params = dict()
    if primary_keys is None:
        primary_keys = DEFAULT_PRIMARY_KEYS
    source_statement = read_sql(
        sql_file=source_statement_file, **source_statement_params
    )
    sql = get_merge_sql(
        client=client,
        project_id=project_id,
        target_dataset=target_dataset,
        target_table=target_table,
        source_statement=source_statement,
        primary_keys=primary_keys,
        mode="INSERT",
        additional_merge_conditions=additional_merge_conditions,
    )
    return query(
        client=client,
        job_config=bigquery.QueryJobConfig(),
        sql=sql,
        timeout=timeout,
        location=location,
    )


def write_query_results_to_destination(
    service_account_file: str,
    sql_file: str,
    timeout: int,
    location: str,
    destination_dataset: str,
    destination_table: str,
    write_disposition: str,
):
    """

    :param service_account_file: relative location of service account file
    :param sql_file: relative location of sql file to read sql from
    :param timeout: job timeout parameter
    :param location: job location parameter
    :param destination_dataset: id of the destination dataset
    :param destination_table: id of the destination table
    :param write_disposition: write disposition of query results
    :return:
    """
    if write_disposition not in WRITE_DISPOSITIONS:
        raise ValueError(
            "Invalid write disposition: {}. Acceptable values are WRITE_APPEND, WRITE_TRUNCATE, and WRITE_EMPTY".format(
                write_disposition
            )
        )
    client = connect(service_account_file)
    job_config = bigquery.QueryJobConfig()
    job_config.write_disposition = write_disposition
    job_config.allow_large_results = True
    job_config.destination = get_table_ref(
        client, destination_dataset, destination_table
    )
    sql = read_sql(sql_file=sql_file)
    return query(client, job_config, sql, timeout, location)


def get_query_results(
    service_account_file: str,
    sql_file: str,
    return_type: str = DEFAULT_RETURN_TYPE,
    sql_params: dict = None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs query and returns the result as dataframe

    :param return_type: file format to be returned (dict,dataframe,json); default is dataframe
    :param service_account_file: relative location of service account file
    :param sql_file: relative location of sql file to read sql from
    :param sql_params: sql parameters dictionary
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return: query result
    """
    client = connect(service_account_file=service_account_file)
    if sql_params is None:
        sql_params = dict()
    sql = read_sql(sql_file=sql_file, **sql_params)
    return select(
        client=client,
        sql=sql,
        timeout=timeout,
        location=location,
        return_type=return_type,
    )


def get_single_value_query_results(
    service_account_file: str,
    sql_file: str,
    sql_params: dict = None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a single value returning query and returns the result

    :param service_account_file: relative location of service account file
    :param sql_file: relative location of sql file to read sql from
    :param sql_params: sql parameters dictionary
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return: query result
    """
    client = connect(service_account_file=service_account_file)
    if sql_params is None:
        sql_params = dict()
    sql = read_sql(sql_file=sql_file, **sql_params)
    return single_value_select(
        client=client,
        sql=sql,
        timeout=timeout,
        location=location,
    )


def delete(
    service_account_file: str,
    project_id: str,
    dataset_id: str,
    table_id: str,
    where_statement_file: str,
    where_statement_params: dict = None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a delete query on given table, and removes rows that conform where condition

    :param service_account_file: relative location of service account file
    :param project_id: Bigquery project id
    :param dataset_id: dataset id
    :param table_id: table id
    :param where_statement_file: relative location of where statement sql file
    :param where_statement_params: parameters of where statements
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return: query result
    """
    client = connect(service_account_file=service_account_file)
    if where_statement_params is None:
        where_statement_params = dict()
    where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
    sql = get_delete_sql(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        where_statement=where_statement,
    )
    return query(
        client=client,
        job_config=bigquery.QueryJobConfig(),
        sql=sql,
        timeout=timeout,
        location=location,
    )


def archive(
    service_account_file: str,
    archive_date: str,
    project_id: str,
    source_dataset: str,
    source_table: str,
    target_dataset: str,
    target_table: str,
    primary_keys: list = None,
    mode: str = "INSERT",
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Archives selected rows on target non-partitioned table.

    :param service_account_file: relative location of service account file
    :param archive_date: archive date
    :param project_id: Bigquery project id
    :param source_dataset: source dataset id
    :param source_table: source table id
    :param target_dataset: target dataset id
    :param target_table: target table id
    :param primary_keys: primary key columns of the source and target tables
    :param mode: archive mode, INSERT only inserts non-existing rows and UPSERT updates and inserts
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return:
    """
    if mode not in ARCHIVE_MODES:
        raise ValueError(
            "Invalid archive mode:{}. Acceptable column names are ".format(mode)
            + COMMA.join(i for i in ARCHIVE_MODES)
        )
    if primary_keys is None:
        primary_keys = ARCHIVE_DEFAULT_PRIMARY_KEYS
    source_statement_params = dict()
    source_statement_params["project_id"] = project_id
    source_statement_params["source_dataset"] = source_dataset
    source_statement_params["source_table"] = source_table
    source_statement_params["archive_date"] = archive_date
    source_statement_params["source_partition_field"] = get_time_partition_field(
        client=connect(service_account_file=service_account_file),
        dataset_id=source_dataset,
        table_id=source_table,
    )
    if mode == "INSERT":
        insert(
            service_account_file=service_account_file,
            source_statement_file=ARCHIVE_SOURCE_STATEMENT_FILE,
            project_id=project_id,
            target_dataset=target_dataset,
            target_table=target_table,
            source_statement_params=source_statement_params,
            primary_keys=primary_keys,
            timeout=timeout,
            location=location,
        )
    elif mode == "UPSERT":
        upsert(
            service_account_file=service_account_file,
            source_statement_file=ARCHIVE_SOURCE_STATEMENT_FILE,
            project_id=project_id,
            target_dataset=target_dataset,
            target_table=target_table,
            source_statement_params=source_statement_params,
            primary_keys=primary_keys,
            timeout=timeout,
            location=location,
        )
    delete_where_statement_params = dict()
    delete_where_statement_params["archive_date"] = archive_date
    delete_where_statement_params["source_partition_field"] = source_statement_params[
        "source_partition_field"
    ]
    delete(
        service_account_file=service_account_file,
        project_id=project_id,
        dataset_id=source_dataset,
        table_id=source_table,
        where_statement_file=ARCHIVE_DELETE_WHERE_STATEMENT_FILE,
        where_statement_params=delete_where_statement_params,
        timeout=timeout,
        location=location,
    )


def list_tables(service_account_file: str, project_id: str, dataset_id: str):
    """
    Returns a list of all tables in a dataset

    :param service_account_file: relative location of service account file
    :param project_id: Bigquery project id
    :param dataset_id: dataset id
    :return: List
    """
    client = connect(service_account_file=service_account_file)
    return query_information_schema(
        client=client,
        requested_column_name="table_name",
        project_id=project_id,
        dataset_id=dataset_id,
    )
