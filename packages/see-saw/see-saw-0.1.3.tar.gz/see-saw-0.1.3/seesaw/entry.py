import asyncio
from asyncio.exceptions import CancelledError
import fnmatch
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from shutil import rmtree
from typing import Any, Callable, List, Tuple, Dict

import boto3
import click
import urwid
from urwid.main_loop import AsyncioEventLoop

from seesaw import storage
from seesaw.config import LOG_DIR, LOG_FILE, SETTINGS, USER_DIR, logger
from seesaw.log_factory import (
    AsyncLogStreamPoller,
    groups_from_region,
    ordered_log_query,
)
from seesaw.transforms import (
    abbreviate_group_name,
    format_event,
    humanize_size,
    localize_timestamp,
    relative_utc_time,
    unmask_group_name,
)

log = logger(__file__)


@click.group(invoke_without_command=True)
@click.option("--region", default=None)
@click.option("-m", "--backfill-minutes", default=30)
@click.pass_context
def cli(ctx, region, backfill_minutes):
    log.info("launched", context=vars(ctx), region=region)
    if not backfill_minutes > 0:
        print("-m/--backfill-minutes must be a positive number")
        sys.exit(1)

    if ctx.invoked_subcommand is None:
        account_id = boto3.client("sts", region_name=region).get_caller_identity()[
            "Account"
        ]
        storage.remove_old(region, account_id, timedelta(days=7))
        try:
            tui_loop(region, account_id, backfill=backfill_minutes)
        except KeyboardInterrupt:
            sys.exit(3)


@cli.command("files")
@click.option("--clear", default=False, is_flag=True)
@click.option("-v", "--verbose", default=False, is_flag=True)
def files(clear, verbose):
    print("Log file", LOG_FILE)
    print("Config file", str(USER_DIR / "config.json"))
    print("Databases", str(USER_DIR / f"*.sqlite"))

    total_size = 0

    for top in (LOG_DIR, USER_DIR):
        for cwd, _, files in os.walk(top):
            cwd = Path(cwd)
            for f in files:
                size = os.stat(cwd / f).st_size
                if verbose:
                    print(humanize_size(size), (cwd / f))
                total_size += size
    print("Total space:", humanize_size(total_size))

    if clear:
        if LOG_DIR.exists():
            print("Deleting seesaw logs")
            rmtree(LOG_DIR)
        if USER_DIR.exists():
            print("Deleting seesaw user data")
            rmtree(USER_DIR)


@cli.command("tail")
@click.option("--region", default=None)
@click.option("-a", "--all-groups", is_flag=True, help="Tail all existing log groups")
@click.option(
    "-l",
    "--list-groups",
    is_flag=True,
    metavar="list_groups",
    help="List groups that would be tailed, then exit. Useful for testing glob patterns.",
)
@click.option(
    "--long-dates/--short-dates",
    is_flag=True,
    help="Show full dates, or shorten to just the time.",
)
@click.argument("LOG_GROUPS", nargs=-1)
def tail(region, all_groups, long_dates, list_groups, log_groups):
    """Pass any number LOG_GROUP names or fnmatch patterns to select log groups.

    - * - matches everything

    - ? - matches any single character

    - [seq] - matches any character in seq

    - [!seq] - matches any character not in seq

    Example: view all lambda logs

    $ seesaw tail '/aws/lambda*'

    Example: view all logs from MyApp log groups, including any Lambda, EC2, or Step Functions groups

    $ seesaw tail '*MyApp*'

    Example: view all API Gateway Execution logs

    $ seesaw tail 'API-Gateway-Exec*'"""
    if region is None:
        region = SETTINGS["presets"]["default"]["region"]
    if not log_groups:
        log_groups = SETTINGS["presets"]["default"]["log_groups"]
    if any(c in "".join(log_groups) for c in list("*[]?!")) or all_groups:
        # if the log groups have any globbing characters in them, run a glob match
        group_list = [g["name"] for g in groups_from_region(region)]
        if all_groups:
            log_groups = group_list
        else:
            matched_groups = [
                group
                for group in group_list
                if any(fnmatch.fnmatchcase(group, pattern) for pattern in log_groups)
            ]

            log_groups = matched_groups
        log.info("Polling all available log groups", groups=log_groups)
    if list_groups:
        for l in log_groups:
            print(l)
        return

    try:
        asyncio.run(tail_loop(region, log_groups, long_dates=long_dates))
    except KeyboardInterrupt:
        pass


async def task_monitor():
    prior = {}
    while True:
        await asyncio.sleep(3)
        states = {t.get_name(): t.done() for t in asyncio.all_tasks()}
        if states != prior:
            log.info(
                "active coroutines",
                tasks=sorted(t.get_name() for t in asyncio.all_tasks()),
                states=states,
                source="task_monitor",
            )
            prior = states


def create_log_group_aio_pollers(region, log_groups, account_id):
    tasks = {t.get_name(): t for t in asyncio.all_tasks()}
    for task_name, coroutine in tasks.items():
        if not task_name.startswith("GroupPoller"):
            continue
        polled_group = task_name.split(" ", 1)[-1]
        if polled_group not in log_groups and not coroutine.done():
            # then we can cancel the aio task
            coroutine.cancel("No longer required")
            log.info(
                "Cancelled polling for group",
                group=polled_group,
                task_name=task_name,
                stack=coroutine.get_stack(),
                cancel_status=coroutine.cancelled(),
            )

    for group in log_groups:
        if any(group in t for t in tasks):
            # there is already a poller for this log group, skip it
            continue
        group_poller = AsyncLogStreamPoller(
            region,
            account_id=account_id,
            start_time=datetime.now(tz=timezone.utc) - timedelta(minutes=5),
        )
        asyncio.create_task(group_poller.slurp_logs(group), name=f"GroupPoller {group}")


async def tail_loop(region, log_groups, long_dates):
    asyncio.create_task(
        task_monitor(),
        name="task_monitor",
    )
    asyncio.current_task().set_name("tail_loop")
    local_account = boto3.client("sts").get_caller_identity()["Account"]
    print("AWS account:", local_account, "region:", region, file=sys.stderr)
    print("groups:", ", ".join(log_groups), file=sys.stderr)
    log.debug(
        "Commencing tail of", region=region, groups=log_groups, account=local_account
    )
    create_log_group_aio_pollers(region, log_groups, local_account)

    async for event in ordered_log_query(
        region, local_account, start_from=timedelta(minutes=5), log_groups=log_groups
    ):
        print(" ".join(format_event(event, verbose_dates=long_dates)).strip())


async def refresh_pane(new_message: Callable, **kwargs):
    sent = 0
    log.debug("refreshing visible logs")
    try:
        async for event in ordered_log_query(**kwargs):
            sent += 1
            log.debug("Pushing event to pane", evt=event.gid, total_this_setting=sent)
            new_message(event)
    except CancelledError:
        pass
    except:
        log.exception("Refresh error")


class LogReadingPane:
    def __init__(self, region: str, account: str, backfill: int) -> None:
        self.backfill = backfill
        self.region = region
        self.account = account
        self.messages = urwid.SimpleFocusListWalker([])
        self.viewer = urwid.ListBox(self.messages)
        self.verbose_dates = False
        self.help_active = False
        self.backfill_tasks: Dict[str, Any] = {}

        self.poller = None

        self.menu = GroupSelect(
            region=region, account=account, groups_changed=self.create_aio_poll_task
        )
        self.top = urwid.Columns([(70, self.menu), self.viewer], dividechars=2)

    def create_aio_poll_task(self, groups):
        if self.poller:
            log.info("Killing poller", t=type(self.poller))
            self.poller.cancel("Replacing with new poller")
            log.debug(
                "Cancelled one", t={t.get_name(): t.done() for t in asyncio.all_tasks()}
            )
            self.messages.clear()
        for g in groups:
            if g in self.backfill_tasks:
                # we already are running backfill
                continue
            # start backfill tasks, breaking up into 15 minute chunks
            self.backfill_tasks[g] = []
            for i in range(0, self.backfill, 15):
                log.info("Backfill", start=i, end=i + 15)
                group_poller = AsyncLogStreamPoller(
                    self.region,
                    account_id=self.account,
                    poll_delay_seconds=1,
                    start_time=relative_utc_time(minutes=-i),
                )
                self.backfill_tasks[g].append(
                    asyncio.create_task(
                        group_poller.slurp_logs(
                            g, end_time=relative_utc_time(minutes=-(i + 15))
                        ),
                        name=f"BackfillPoller {i}-{i+15} {g}",
                    )
                )

        self.poller = asyncio.get_running_loop().create_task(
            refresh_pane(
                new_message=self.new_message,
                start_from=timedelta(hours=2),
                region=self.region,
                account_id=self.account,
                log_groups=groups,
            ),
            name=f"pane-refresher-{datetime.now().strftime('%H:%M:%S.%f')}",
        )

    def new_message(self, event):
        if len(self.messages) > 500:
            self.messages.pop(0)
        self.messages.append(urwid.Text(self.format_event(event)))
        self.viewer.focus_position = len(self.messages) - 1

    def toggle_date(self):
        self.verbose_dates = not self.verbose_dates

    def help_popup(self):
        self.help_active = not self.help_active

    def timestamp(self, ts):
        if self.verbose_dates:
            return (
                "timestamp",
                localize_timestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
            )
        return (
            "timestamp",
            localize_timestamp(ts).strftime("%H:%M:%S"),
        )

    def format_event(self, event: storage.Event):
        try:

            return [
                self.timestamp(event.timestamp),
                " ",
                abbreviate_group_name(event.log_group),
                " ",
                json.dumps(json.loads(event.message), indent=2, sort_keys=True),
            ]
        except:
            return [
                self.timestamp(event.timestamp),
                " ",
                abbreviate_group_name(event.log_group),
                " ",
                event.message,
            ]


class GroupSelect(urwid.WidgetWrap):
    def __init__(self, account: str, region: str, groups_changed: Callable):
        self.region = region
        self.account = account
        self.selected_groups = set()
        self.groups_changed = groups_changed
        urwid.WidgetWrap.__init__(self, self.build_group_checkboxes(region))

    def toggle_group_select(self, widget, active: bool):
        log.info(
            "log group selected",
            value=active,
            group_name=unmask_group_name(widget.get_label()),
        )
        if active:
            self.selected_groups.add(unmask_group_name(widget.get_label()))
        else:
            self.selected_groups.remove(unmask_group_name(widget.get_label()))

        create_log_group_aio_pollers(
            self.region, list(self.selected_groups), self.account
        )
        self.groups_changed(list(self.selected_groups))

    def get_state(self):
        return list(self.selected_groups)

    def build_group_checkboxes(self, region_name: str):
        return urwid.ListBox(
            [
                urwid.CheckBox(
                    abbreviate_group_name(g["name"]),
                    on_state_change=self.toggle_group_select,
                )
                for g in groups_from_region(region_name)
            ]
        )


def key_handler(sawmill):
    def show_or_exit(key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop
        elif key in ("h", "H"):
            sawmill.help_popup()
        elif key in ("v", "V"):
            sawmill.toggle_date()
        elif key in ("c", "C"):
            sawmill.messages.clear()
        elif key in ("G"):
            # go to the last message
            sawmill.viewer.set_focus(len(sawmill.messages) - 1)
        elif key in ("g"):
            # go to the top of the page
            sawmill.viewer.set_focus(0)

    return show_or_exit


def tui_loop(region, account, backfill):
    aio_loop = asyncio.get_event_loop()
    reader = LogReadingPane(region=region, account=account, backfill=backfill)
    aio_loop.create_task(
        task_monitor(),
        name="task_monitor",
    )
    loop = urwid.MainLoop(
        reader.top,
        {
            ("timestamp", "dark red", "light gray"),
        },
        event_loop=AsyncioEventLoop(loop=aio_loop),
        unhandled_input=key_handler(reader),
    )
    loop.run()
