import json
import random
from datetime import datetime, timedelta, timezone
from typing import Tuple

from dateutil import tz

localtz = tz.tzlocal()


def relative_utc_time(td: timedelta = None, **kwargs) -> datetime:
    if td and not isinstance(td, timedelta):
        raise ValueError(
            "Positional arguments are only for timedeltas, for pass-through values to timedelta us kwargs"
        )
    if td is None:
        td = timedelta(**kwargs)
    return datetime.now(tz=timezone.utc) + td


def relative_iso_time(td: timedelta = None, **kwargs) -> str:
    return relative_utc_time(td, **kwargs).isoformat()


def localize_timestamp(iso_format_dt: str) -> datetime:
    return datetime.fromisoformat(iso_format_dt).astimezone(localtz)


def abbreviate_group_name(name: str) -> str:
    if name.startswith("/aws/lambda/"):
        return name.replace("/aws/lambda/", "λ ")
    if name.startswith("/aws/vendedlogs/states/"):
        return name.replace("/aws/vendedlogs/states/", "SF ")
    if name.startswith("API-Gateway-Execution-Logs_"):
        return name.replace("API-Gateway-Execution-Logs_", "API-Exec-")
    return name


def unmask_group_name(name: str) -> str:
    if name.startswith("λ "):
        return name.replace("λ ", "/aws/lambda/")
    if name.startswith("SF "):
        return name.replace("SF ", "/aws/vendedlogs/states/")
    if name.startswith("API-Exec-"):
        return name.replace("API-Exec-", "API-Gateway-Execution-Logs_")
    return name


def random_hex():
    return "".join(random.choice("abcdef1234567890") for _ in range(10))


def humanize_size(total_size):
    for x in ("bytes", "KB", "MB", "GB", "TB"):
        if total_size < 1024.0:
            return "%.1f %s" % (total_size, x)
        total_size /= 1024.0

    return "%.1f %s" % (total_size, x)


def format_event(event, verbose_dates=True) -> Tuple[str, str]:
    ts = localize_timestamp(event.timestamp)
    if verbose_dates:
        ts = ts.strftime("%Y-%m-%d %H:%M:%S")
    else:
        ts = ts.strftime("%H:%M:%S")

    try:
        return (
            ts,
            abbreviate_group_name(event.log_group),
            json.dumps(json.loads(event.message), indent=2, sort_keys=True),
        )
    except json.decoder.JSONDecodeError:
        return ts, abbreviate_group_name(event.log_group), event.message
