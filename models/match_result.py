from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    influencer_id = Column(Integer, ForeignKey("influencer_profiles.id"), nullable=False)

    score = Column(Float, nullable=False)
    reason = Column(String, nullable=True)  # breakdown string, e.g. "category:50 budget:30 engagement:20"

    campaign = relationship("Campaign", backref="matches")
    influencer = relationship("InfluencerProfile", backref="matches")