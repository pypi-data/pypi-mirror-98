import json
import logging
import os
import pathlib
from logging.handlers import RotatingFileHandler
from pathlib import Path

import appdirs
import structlog
import structlog.contextvars

APP_NAME = "seesaw"
APP_AUTHOR = "ryansb"
VERSION = "0.1.3"

USER_DIR = Path(appdirs.user_config_dir(appname=APP_NAME, appauthor=APP_AUTHOR))
LOG_DIR = Path(appdirs.user_log_dir(appname=APP_NAME, appauthor=APP_AUTHOR))

CONF_DEFAULTS = {
    "schema": "0.1",
    "presets": {
        "default": {
            "region": "us-east-1",
            "log_groups": [
                "/aws/apigateway/welcome",
            ],
        },
    },
}

if not LOG_DIR.is_dir():
    LOG_DIR.mkdir(parents=True)
if not USER_DIR.is_dir():
    USER_DIR.mkdir(parents=True)
if not (USER_DIR / "config.json").exists():
    with open(USER_DIR / "config.json", "w") as cfg:
        json.dump(CONF_DEFAULTS, cfg, sort_keys=True, indent=2)

with open(USER_DIR / "config.json", "r") as cfg:
    SETTINGS = json.load(cfg)
LOG_FILE = str(LOG_DIR / f"logs-{VERSION}.json")

root = logging.getLogger()


log_level = logging.WARN

logging.basicConfig(
    format="%(message)s",
    handlers=[
        RotatingFileHandler(
            LOG_FILE,
            # limit each log file to 2MB
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
        )
    ],
    level=log_level,
)

logging.getLogger("seesaw").setLevel(
    logging.DEBUG if os.getenv("SEESAW_DEBUG") else logging.INFO
)
logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
structlog.configure(
    processors=[
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(utc=False, key="timestamp", fmt="iso"),
        structlog.contextvars.merge_contextvars,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

_log_cache = {}


def logger(calling_file: str, context: dict = None) -> structlog.BoundLogger:
    """usage: logger(__file__, {})"""
    path = pathlib.Path(calling_file).parts
    try:
        logger_path = ".".join(path[path.index("seesaw") + 1 :]).replace(".py", "")
    except ValueError:
        # called from outside our package
        logger_path = calling_file.replace("/", ".").replace(".py", "")
    if logger_path not in _log_cache:
        _log_cache[logger_path] = structlog.get_logger(logger_path, **(context or {}))
        return _log_cache[logger_path]
    if context:
        _log_cache[logger_path] = _log_cache[logger_path].new(**context)
    return _log_cache[logger_path]
