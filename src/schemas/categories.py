
from pydantic import BaseModel,ConfigDict, Field

class CategoriesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category_id: int
    name: str

class CategoriesCreate(BaseModel):
    name: str = Field(min_length=3 , max_length=64)

class CategoriesUpdate(BaseModel):
    name: str | None = Field(default= None , min_length= 3 , max_length=64)