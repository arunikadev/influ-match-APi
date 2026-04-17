from pydantic import BaseModel
from schemas.influencer_schema import InfluencerProfileResponse


class MatchResultItem(BaseModel):
    influencer: InfluencerProfileResponse
    score: float
    reason: str  # detail breakdown scoring

    class Config:
        from_attributes = True


class MatchResultResponse(BaseModel):
    campaign_id: int
    campaign_title: str
    total_matches: int
    results: list[MatchResultItem]
