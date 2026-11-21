from pydantic import BaseModel, ConfigDict, Field


class SupplierCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    contact: str | None = Field(default=None ,min_length=3, max_length=100)

class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None ,min_length=3, max_length=100)
    contact: str| None = Field(default= None ,min_length=3, max_length=100)

class SupplierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    supplier_id: int
    name: str
    contact: str | None
