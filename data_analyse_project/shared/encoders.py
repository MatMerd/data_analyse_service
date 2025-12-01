import base64
import dataclasses
import json
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

import orjson


class FriendlyEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:  # noqa: C901, PLR0911
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            # The ordering prioritizes the most frequently encountered types first,
            # which should provide better performance in typical use cases.

            # Most common datetime objects first
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            if isinstance(obj, time):
                return obj.strftime("%H:%M:%S")

            # Very common built-in types
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, Decimal):
                return str(obj)

            # Common serializable objects
            if dataclasses.is_dataclass(obj):
                return dataclasses.asdict(obj)  # type:ignore[arg-type]
            if hasattr(obj, "model_dump"):  # Pydantic v2
                return obj.model_dump()
            if hasattr(obj, "dict"):  # Pydantic v1 or similar
                return obj.dict()

            # Less common types
            if isinstance(obj, timedelta):
                return obj.total_seconds()
            if isinstance(obj, bytes):
                return base64.urlsafe_b64encode(obj).decode("utf8")
            raise


def json_dumps(obj: Any) -> str:
    # не умеет дампить в строку, только в байты. Поэтому приходится конвертить обратно
    return orjson.dumps(obj, default=FriendlyEncoder.default).decode()  # type:ignore[arg-type]


def json_loads(obj: Any) -> Any:
    return orjson.loads(obj)
