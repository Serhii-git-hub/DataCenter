from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, computed_field


class PartRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    part_id: int
    category_id: int
    name: str
    sku: str
    price: Decimal
    quantity: int
    reserved: int
    min_stock: int

    @computed_field
    @property
    def available(self) -> int:
        return self.quantity - self.reserved

class PartCreate(BaseModel):
    category_id: int
    name: str = Field(min_length=3, max_length = 64)
    sku: str = Field(min_length=3, max_length = 64)
    price: Decimal = Field(ge=0, decimal_places=2, max_digits=10)
    min_stock: int = Field(ge=0)

class PartUpdate(BaseModel):
    category_id: int | None = None
    name: str | None= Field(default = None,min_length=3, max_length=64)
    sku: str | None = Field(default = None,min_length=3, max_length=64)
    price: Decimal | None= Field(default = None,ge=0 , decimal_places=2, max_digits=10)
    min_stock: int | None = Field(default = None,ge=0)

