import os


here = os.path.abspath(os.path.dirname(__file__))


ARCHIVE_DELETE_WHERE_STATEMENT_FILE = os.path.join(
    here, "bigquery/archive/delete_where_statement.sql"
)
ARCHIVE_SOURCE_STATEMENT_FILE = os.path.join(
    here, "bigquery/archive/source_statement.sql"
)
DEDUPLICATION_GET_OLDEST_PARTITION_FIELD_SQL_FILE = os.path.join(
    here, "bigquery/deduplication/get_oldest_partition_field.sql"
)
DEDUPLICATION_MERGE_KEYS_PARTITION_PRUNING_PARAMS = os.path.join(
    here, "bigquery/deduplication/merge_keys_partition_pruning_params.sql"
)
DEDUPLICATION_SOURCE_STATEMENT_SQL_FILE = os.path.join(
    here, "bigquery/deduplication/source_statement.sql"
)
DEDUPLICATION_SOURCE_WHERE_STATEMENT_SQL_FILE = os.path.join(
    here, "bigquery/deduplication/source_where_statement.sql"
)
DEDUPLICATION_SOURCE_WHERE_STATEMENT_PARTITION_PRUNING_PARAMS_SQL_FILE = os.path.join(
    here, "bigquery/deduplication/source_where_statement_partition_pruning_params.sql"
)
DELETE_SQL_FILE = os.path.join(here, "bigquery/dml/delete.sql")
GET_COLUMN_NAMES_SQL_FILE = os.path.join(
    here, "bigquery/information_schema/get_column_names.sql"
)
GET_TABLE_NAMES_SQL_FILE = os.path.join(
    here, "bigquery/information_schema/get_table_names.sql"
)
INSERT_SQL_FILE = os.path.join(here, "bigquery/dml/insert.sql")
UPSERT_SQL_FILE = os.path.join(here, "bigquery/dml/upsert.sql")
