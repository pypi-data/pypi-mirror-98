from typing import List
from datetime import datetime
from pydantic import BaseModel, conint, constr, StrictInt, StrictStr

from .attachment_meta import AttachmentMeta

MAX_LEN_NON_HASHED = 256

SERVICE_KEYS = [
    "record_key",
    "profile_key",
    "service_key1",
    "service_key2",
]

SEARCH_KEYS = [
    "key1",
    "key2",
    "key3",
    "key4",
    "key5",
    "key6",
    "key7",
    "key8",
    "key9",
    "key10",
]

INT_KEYS = [
    "range_key1",
    "range_key2",
    "range_key3",
    "range_key4",
    "range_key5",
    "range_key6",
    "range_key7",
    "range_key8",
    "range_key9",
    "range_key10",
    "version",
]


class Record(BaseModel):
    record_key: constr(strict=True, min_length=1)
    body: StrictStr = None
    precommit_body: StrictStr = None
    profile_key: StrictStr = None
    service_key1: StrictStr = None
    service_key2: StrictStr = None
    key1: StrictStr = None
    key2: StrictStr = None
    key3: StrictStr = None
    key4: StrictStr = None
    key5: StrictStr = None
    key6: StrictStr = None
    key7: StrictStr = None
    key8: StrictStr = None
    key9: StrictStr = None
    key10: StrictStr = None
    range_key1: StrictInt = None
    range_key2: StrictInt = None
    range_key3: StrictInt = None
    range_key4: StrictInt = None
    range_key5: StrictInt = None
    range_key6: StrictInt = None
    range_key7: StrictInt = None
    range_key8: StrictInt = None
    range_key9: StrictInt = None
    range_key10: StrictInt = None
    version: conint(ge=0, strict=True) = None
    created_at: datetime = None
    updated_at: datetime = None
    attachments: List[AttachmentMeta] = None


class RecordNonHashed(Record):
    key1: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key2: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key3: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key4: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key5: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key6: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key7: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key8: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key9: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
    key10: constr(strict=True, min_length=0, max_length=MAX_LEN_NON_HASHED) = None
