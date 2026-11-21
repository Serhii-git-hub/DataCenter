from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["diagnostic", "waiting_parts", "in_process", "done", "issued"]


class RepairRequestCreate(BaseModel):
    client_name: str = Field(min_length=3, max_length=100)
    phone: str = Field(min_length=3, max_length=32)
    device: str = Field(min_length=3, max_length=100)
    fault_description: str = Field(min_length=3, max_length=1000)


class RepairRequestUpdate(BaseModel):
    client_name: str | None = Field(default=None, min_length=3, max_length=100)
    phone: str | None = Field(default=None, min_length=3, max_length=32)
    device: str | None = Field(default=None, min_length=3, max_length=100)
    fault_description: str | None = Field(default=None, min_length=3, max_length=1000)
    status: Status | None = None


class RepairRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    request_id: int
    user_id: int
    client_name: str
    phone: str
    device: str
    fault_description: str
    status: Status
    created_at: datetime