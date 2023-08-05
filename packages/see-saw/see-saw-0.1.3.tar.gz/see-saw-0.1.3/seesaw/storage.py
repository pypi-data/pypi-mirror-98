import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from seesaw import transforms

import aql
import psutil
from aql import column
from aql.table import table as aql_table
from unsync import unsync

from seesaw.config import USER_DIR, VERSION, logger

log = logger(__file__)


def connect(region: str, account_id: str) -> aql.engines.base.Connection:
    log_db_file = "sqlite://" + str(
        USER_DIR / f"logs-{region}-{account_id}-{VERSION}.sqlite"
    )
    log.debug("Opening DB", path=log_db_file)
    mk_tables(log_db_file)
    return aql.connect(log_db_file)


@unsync
async def remove_old(region: str, account_id: str, max_age: timedelta):
    async with connect(region, account_id) as db:
        await db.execute(
            Event.delete().where(
                Event.timestamp < transforms.transforms.relative_iso_time(td=-max_age)
            )
        )


@unsync
async def mk_tables(db_file):
    connection = aql.connect(db_file)
    create_query = Event.create(if_not_exists=True)
    async with connection as db:
        await db.execute(create_query)


@aql_table("events")
class Event:
    gid: column.Primary[str]
    timestamp: str
    ingestion_time: str
    message: str
    region: str
    account_id: str
    log_group: str
    log_stream: str
    # future use, intended to help add Lambda/SF Execution ID to a special column to support selecting down to one execution
    execution_correlator: Optional[str]


def json_to_event(incoming: dict):
    return Event(
        gid=incoming["eventId"],
        account_id=incoming["accountId"],
        timestamp=datetime.fromtimestamp(
            incoming["timestamp"] / 1000, tz=timezone.utc
        ).isoformat(),
        ingestion_time=datetime.fromtimestamp(
            incoming["ingestionTime"] / 1000, tz=timezone.utc
        ).isoformat(),
        region=incoming["region"],
        message=incoming["message"],
        log_stream=incoming["logStreamName"],
        log_group=incoming["logGroupName"],
        execution_correlator=None,
    )


def get_pid_start_iso() -> str:
    """Return the iso-formatted time the current process started.

    This helps us clear out old thread signatures"""
    pid_start_ts = psutil.Process(os.getpid()).create_time()
    return (
        datetime.utcfromtimestamp(pid_start_ts).replace(tzinfo=timezone.utc).isoformat()
    )
