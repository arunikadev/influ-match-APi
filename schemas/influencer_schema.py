from pydantic import BaseModel, Field
from typing import Optional


class InfluencerProfileCreate(BaseModel):
    niche: str = Field(..., example="food")
    followers: int = Field(..., ge=0, example=50000)
    engagement_rate: float = Field(..., ge=0.0, le=100.0, example=3.5)
    price_rate: float = Field(..., ge=0.0, example=500000.0)
    platform: Optional[str] = Field("instagram", example="instagram")


class InfluencerProfileUpdate(BaseModel):
    niche: Optional[str] = None
    followers: Optional[int] = Field(None, ge=0)
    engagement_rate: Optional[float] = Field(None, ge=0.0, le=100.0)
    price_rate: Optional[float] = Field(None, ge=0.0)
    platform: Optional[str] = None


class InfluencerProfileResponse(BaseModel):
    id: int
    user_id: int
    niche: str
    followers: int
    engagement_rate: float
    price_rate: float
    platform: str

    class Config:
        from_attributes = True
