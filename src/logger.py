import json
import logging
from functools import wraps
from logging import Formatter, LogRecord, INFO, Filter
from typing import override, Callable
import datetime as dt

from pydantic.json import pydantic_encoder
from starlette.responses import Response

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class JsonFormatter(Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: LogRecord):
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str, ensure_ascii=False)

    def _prepare_log_dict(self, record: LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


logger = logging.getLogger("main")


def apilogging(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response: Response = func(*args, **kwargs)
        req = dict()
        for key, value in kwargs.items():
            if key == 'self':
                continue
            req[key] = value
        req_log = json.dumps(req, default=pydantic_encoder, ensure_ascii=False)
        req_log = json.loads(req_log)
        res_log = json.dumps(response, default=pydantic_encoder, ensure_ascii=False)
        res_log = json.loads(res_log)
        logger.info({
            "request_params": req_log,
            "response": res_log
        })
        return response

    return wrapper


class NonErrorFilter(Filter):
    @override
    def filter(self, record: LogRecord) -> bool | LogRecord:
        return record.levelno <= INFO
