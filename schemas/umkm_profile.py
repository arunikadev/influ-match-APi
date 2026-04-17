from pydantic import BaseModel, Field
from typing import Optional


class UMKMProfileCreate(BaseModel):
    business_name: str = Field(..., min_length=2, example="Toko Matcha Sejahtera")
    category: str = Field(..., example="food")
    description: Optional[str] = Field(None, example="Jualan matcha premium dari Jepang")


class UMKMProfileResponse(BaseModel):
    id: int
    user_id: int
    business_name: str
    category: str
    description: Optional[str]

    class Config:
        from_attributes = True
