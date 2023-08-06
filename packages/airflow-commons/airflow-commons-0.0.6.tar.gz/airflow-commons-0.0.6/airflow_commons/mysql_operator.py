from airflow_commons.utils.mysql_utils import upsert, get_db_engine
import airflow_commons.logger as logger


def write_to_mysql(
    username: str,
    password: str,
    host: str,
    db_name: str,
    values: dict,
    chunk_size: int,
    table_name: str,
):
    """

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param values: values to write into database
    :param chunk_size: data size to upload at a time
    :param table_name: database table name to write
    :return:
    """
    engine = get_db_engine(username, password, host, db_name)
    chunks = [values[i : i + chunk_size] for i in range(0, len(values), chunk_size)]
    logger.LOGGER("Chunk size is {}.".format(chunk_size))
    with engine.connect() as conn:
        i = 0
        for chunk in chunks:
            i += 1
            upsert(values=chunk, conn=conn, table_name=table_name)
            logger.LOGGER("Chunk {} uploaded".format(i))
    logger.LOGGER("Data uploaded to MySql.")
