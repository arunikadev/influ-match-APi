from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CampaignCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, example="Promosi Matcha Bulan Ramadan")
    category_target: str = Field(..., example="food")
    budget: float = Field(..., gt=0, example=1000000.0)
    description: Optional[str] = Field(None, example="Campaign untuk promosi produk matcha premium")


class CampaignUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    category_target: Optional[str] = None
    budget: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    status: Optional[str] = Field(None, example="closed")


class CampaignResponse(BaseModel):
    id: int
    umkm_id: int
    title: str
    category_target: str
    budget: float
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
