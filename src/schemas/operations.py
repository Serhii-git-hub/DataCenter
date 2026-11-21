from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

OperationType = Literal["receipt", "reserve", "issue", "unreserve", "write_off"]


class OperationCreate(BaseModel):
    part_id: int
    type: OperationType
    quantity: int = Field(gt=0)
    supplier_id: int | None = None
    request_id: int | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    reason: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def check_links(self):
        if self.type == "receipt" and self.supplier_id is None:
            raise ValueError("Для receipt потрібен supplier_id")
        if self.type in ("reserve", "issue", "unreserve") and self.request_id is None:
            raise ValueError("Для reserve/issue/unreserve потрібен request_id")
        return self


class OperationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    operation_id: int
    part_id: int
    user_id: int
    supplier_id: int | None
    request_id: int | None
    type: OperationType
    quantity: int
    price: Decimal | None
    reason: str | None
    created_at: datetime