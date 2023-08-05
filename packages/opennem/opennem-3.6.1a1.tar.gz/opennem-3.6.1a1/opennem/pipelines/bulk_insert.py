"""
OpenNEM Bulk Insert Pipeline

Bulk inserts records using temporary tables and CSV imports with copy_from

This is by far the fastest way to bulk insert large records sets of consistent width
and supports on conflict upserts with postgres

This should be the last step of the pipeline and requires `RecordsToCSVPipeline`
from `csv.py`

@TODO use pydantic throughout to tidy up the schema that is passed through the pipeline

"""
import logging
from datetime import datetime
from io import StringIO
from typing import Any, List, Optional, Union

# from sqlalchemy.exc import StatementError
from sqlalchemy.sql.schema import Column, Table

from opennem.db import get_database_engine
from opennem.utils.pipelines import check_spider_pipeline

logger = logging.getLogger(__name__)

BULK_INSERT_QUERY = """
    CREATE TEMP TABLE __tmp_{table_name}_{tmp_table_name}
    (LIKE {table_name} INCLUDING DEFAULTS)
    ON COMMIT DROP;

    COPY __tmp_{table_name}_{tmp_table_name} FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

    INSERT INTO {table_name}
        SELECT *
        FROM __tmp_{table_name}_{tmp_table_name}
    ON CONFLICT {on_conflict}
"""

BULK_INSERT_CONFLICT_UPDATE = """
    ({pk_columns}) DO UPDATE set {update_values}
"""


def build_insert_query(
    table: Table,
    update_cols: List[Union[str, Column]] = None,
) -> str:
    """
    Builds the bulk insert query
    """
    on_conflict = "DO NOTHING"

    def get_column_name(column: Union[str, Column]) -> str:
        if isinstance(column, Column) and hasattr(column, "name"):
            return column.name
        if isinstance(column, str):
            return column.strip()
        return ""

    update_col_names = []

    if update_cols:
        update_col_names = [get_column_name(c) for c in update_cols]

    update_col_names = list(filter(lambda c: c, update_col_names))

    primary_key_columns = [c.name for c in table.__table__.primary_key.columns.values()]

    if len(update_col_names):
        on_conflict = BULK_INSERT_CONFLICT_UPDATE.format(
            pk_columns=",".join(primary_key_columns),
            update_values=", ".join([f"{n} = EXCLUDED.{n}" for n in update_col_names]),
        )

    query = BULK_INSERT_QUERY.format(
        table_name=table.__table__.name,
        on_conflict=on_conflict,
        tmp_table_name=datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"),
    )

    logger.debug(query)

    return query


class BulkInsertPipeline(object):
    @check_spider_pipeline
    def process_item(self, item: List[dict], spider):
        num_records = 0
        conn = get_database_engine().raw_connection()

        if not isinstance(item, list):
            spider_name = "unknown"

            if spider and hasattr(spider, "name"):
                spider_name = spider.name

            logger.error(
                "Did not get a list of items in bulk inserter from spider {}".format(spider_name)
            )

            return {"num_records": "ERROR"}

        for single_item in item:
            if "csv" not in single_item:
                logger.error("No csv record passed to bulk inserter")
                return 0

            csv_content: StringIO = single_item["csv"]

            if "table_schema" not in single_item:
                logger.error("No table model passed to bulk inserter")
                return item

            table: Table = single_item["table_schema"]

            update_fields: Optional[List[Union[str, Column[Any]]]] = None

            if "update_fields" in single_item:
                update_fields = single_item["update_fields"]

            sql_query = build_insert_query(table, update_fields)

            try:
                cursor = conn.cursor()
                cursor.copy_expert(sql_query, csv_content)
                conn.commit()
            except Exception as generic_error:
                if hasattr(generic_error, "hide_parameters"):
                    generic_error.hide_parameters = True
                logger.error(generic_error)

            try:
                num_records += len(csv_content.getvalue().split("\n")) - 1
            except Exception:
                pass

        return {"num_records": num_records}
