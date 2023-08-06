from enum import Enum

from datetime import datetime
from dateutil import rrule, tz
from dateutil.utils import default_tzinfo
from pydantic import validator, Field
from typing import List, Optional

from openmodule import config
from openmodule.models.base import OpenModuleModel, ZMQMessage, Gateway, timezone_validator


class Medium(str, Enum):
    LPR = "lpr"
    NFC = "nfc"
    PIN = "pin"
    QR = "qr"


class Category(str, Enum):
    BOOKED_DIGIMON = "booked-digimon"
    BOOKED_EMPLOYEE = "booked-employee"
    BOOKED_VISITOR = "booked-visitor"
    PERMANENT_DIGIMON = "permanent-digimon"
    PERMANENT_EMPLOYEE = "permanent-employee"
    FILLER_EMPLOYEE = "filler-employee"
    FILLER_DIGIMON = "filler-digimon"
    FILLER_VISITOR_BUTTON = "filler-visitor-button"
    FILLER_VISITOR_UNEXPECTED = "filler-visitor-unexpected"
    UNKNOWN_CATEGORY = "unknown-category"


class AccessRequest(OpenModuleModel):
    """
    The AccessRequest Model
    """
    name: str
    gateway: Optional[Gateway] = None
    medium_type: Medium
    id: str


def check_recurrence(cls, recurrence, values, **kwargs):
    if recurrence is not None:
        if not values.get("duration"):
            raise ValueError("set a duration when using recurrence")

        try:
            if "DTSTART" not in recurrence:
                raise ValueError("recurrence must contain a DTSTART field")

            if "\n" not in recurrence:
                raise ValueError("DTSTART must be separated by a newline '\\n' character")

            rrule.rrulestr(recurrence)
        except Exception as e:
            raise ValueError(f"recurrence is not valid '{e}'") from None
        return recurrence
    else:
        return None


class Access(OpenModuleModel):
    category: Category
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[int] = Field(description="duration in seconds, starting with the start time of the "
                                                "recurrence. Required if recurrence is set.")
    recurrence: Optional[str]
    zone: Optional[str]
    occupant_check: bool = False
    infos: Optional[dict] = {}
    user: str

    _check_recurrence = validator("recurrence", allow_reuse=True)(check_recurrence)
    _check_start = timezone_validator("start")
    _check_end = timezone_validator("end")

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data["start"] = data["start"].timestamp()
        if data.get("end") is not None:
            data["end"] = data["end"].timestamp()
        return data

    def is_valid_at(self, dt, timezone):
        dt = default_tzinfo(dt, tz.UTC)
        if self.recurrence:
            assert False, "recurrent accesses are not yet supported"
        else:
            if self.end:
                return self.start <= dt <= self.end
            else:
                return self.start <= dt


class MediumAccesses(OpenModuleModel):
    accesses: List[Access]
    id: str
    type: str


class AccessResponse(OpenModuleModel):
    success: bool = False
    medium: MediumAccesses


class CountMessage(ZMQMessage):
    resource: str = config.resource()
    user: str
    gateway: Gateway
    medium_type: Medium
    id: str
    count: int
    transaction_id: str
    zone: str
    category: Category
    real: bool
    access_data: Optional[dict]
    error: Optional[str]
    previous_transaction_id: Optional[List[str]]  # double_entry, choose_random error
    previous_user: Optional[str]  # user_changed error
    previous_medium_type: Optional[str]  # medium_changed, medium_id_changed error
    previous_id: Optional[str]  # medium_changed, medium_id_changed error
    chosen: Optional[dict]  # choose_random error
