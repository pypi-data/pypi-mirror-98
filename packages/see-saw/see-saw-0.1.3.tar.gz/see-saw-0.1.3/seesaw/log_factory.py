import asyncio
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import List

import boto3

from seesaw import storage
from seesaw.config import logger
from seesaw.transforms import humanize_size, localize_timestamp, relative_iso_time

log = logger(__file__)


def _pagination_coro(iterable):
    try:
        if page := next(iterable):
            return page
    except StopIteration:
        pass
    return {"events": []}


async def ordered_log_query(
    region: str,
    account_id: str,
    log_groups: List[str],
    start_from: timedelta = timedelta(minutes=5),
):
    """async coroutine that yields timestamp-ordered query from any log DB"""
    timestamp = relative_iso_time(-start_from)
    log.info(
        "Started query stack",
        region=region,
        account_id=account_id,
        log_groups=log_groups,
        start_from=start_from,
        start_ts=timestamp,
        local_start_ts=localize_timestamp(timestamp).isoformat(),
    )
    async with storage.connect(region, account_id) as db:
        events_yielded = {}
        while True:
            async for event in db.execute(
                storage.Event.select()
                .where(storage.Event.account_id == account_id)
                .where(storage.Event.timestamp > timestamp)
                .where(storage.Event.region == region)
                .where(storage.Event.log_group.in_(log_groups))
                .orderby(storage.Event.timestamp)
            ):
                if event.gid not in events_yielded:
                    yield event
                    events_yielded[event.gid] = event.timestamp

            await asyncio.sleep(1)
            if len(events_yielded) > 2000:
                expired_ts = relative_iso_time(-(start_from + timedelta(minutes=1)))
                for k in list(events_yielded.keys()):
                    if events_yielded[k] < expired_ts:
                        events_yielded.pop(k)
                log.info("Trimmed printed event cache")

            # since we poll the log groups every five seconds, give a grace
            # period of 3 polls for every paginator to get its data in
            timestamp = relative_iso_time(seconds=-15)


def groups_from_region(region_name):
    """All log group names that ARE NOT empty and older than 8 hours"""
    logs = boto3.client("logs", region_name=region_name)
    try:
        pager = (
            logs.get_paginator("describe_log_groups")
            .paginate()
            .search(
                "logGroups[].{name: logGroupName, size: storedBytes, created: creationTime}"
            )
        )
        for group in pager:
            since_created = datetime.now(tz=timezone.utc) - datetime.fromtimestamp(
                group["created"] / 1000, tz=timezone.utc
            )

            log.debug(
                "Discovered log group",
                region=region_name,
                name=group["name"],
                size=humanize_size(group.get("size") or 0),
            )

            if group["size"] or since_created < timedelta(hours=8):
                group["region"] = region_name
                yield group
    except logs.exceptions.UnrecognizedClientException:
        pass


class AsyncLogStreamPoller:
    def __init__(
        self,
        region: str,
        account_id: str,
        logs_client: boto3.client = None,
        poll_delay_seconds: int = 5,
        start_time: datetime = None,
    ):
        self.poll_delay_seconds = poll_delay_seconds
        self.region = region
        self.account_id = account_id
        self.start_time = start_time or datetime.now(tz=timezone.utc)
        self.logs = logs_client or boto3.client("logs", region_name=region)

    async def slurp_logs(
        self,
        group_name: str,
        start_time: datetime = None,
        end_time: datetime = None,
    ):
        kwargs = {
            "logGroupName": group_name,
            "interleaved": True,
        }
        if end_time is not None:
            kwargs["endTime"] = int(end_time.timestamp()) * 1000
        if start_time is None:
            kwargs["startTime"] = int(self.start_time.timestamp()) * 1000
        else:
            kwargs["startTime"] = int(start_time.timestamp()) * 1000
        while True:
            log.debug("Calling log filter", kwargs=kwargs)
            iterable = iter(
                self.logs.get_paginator("filter_log_events").paginate(**kwargs)
            )
            while True:
                page = await asyncio.get_running_loop().run_in_executor(
                    None, _pagination_coro, iterable
                )
                if not page["events"]:
                    # if a page is empty, bail
                    await asyncio.sleep(self.poll_delay_seconds)
                    break
                log.debug(
                    "Got page for",
                    group=group_name,
                    events=len(page["events"]),
                    start=kwargs["startTime"],
                    end=kwargs.get("endTime"),
                )
                incoming_events = sorted(
                    page["events"],
                    key=lambda e: e["timestamp"],
                )
                # update the start time to when we start paginating through
                kwargs["startTime"] = int(
                    max(incoming_events[-1]["timestamp"] / 1000, kwargs["startTime"])
                )
                async with storage.connect(self.region, self.account_id) as db:
                    for event in incoming_events:
                        event["logGroupName"] = group_name
                        event["region"] = self.region
                        event["accountId"] = self.account_id
                        try:
                            await db.execute(
                                storage.Event.insert().values(
                                    storage.json_to_event(event)
                                )
                            )
                        except sqlite3.IntegrityError as e:
                            if "UNIQUE constraint failed: events.gid" in repr(e):
                                # we expect to sometimes double-write events, nothing to worry about
                                continue
                            log.exception(
                                "SQLite integrity problem for event",
                                gid=event["eventId"],
                                msg=event["message"],
                                stream=event["logStreamName"],
                                group=event["logGroupName"],
                            )
                    await db.commit()
            if end_time:
                # only go through one query if there is an end time specified
                log.info(
                    "Finished backfill",
                    group=group_name,
                    start=kwargs["startTime"],
                    end=kwargs["endTime"],
                )
                break
            await asyncio.sleep(self.poll_delay_seconds)
