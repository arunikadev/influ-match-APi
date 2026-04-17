from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class InfluencerProfile(Base):
    __tablename__ = "influencer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    niche = Column(String, nullable=False)          # e.g. "food", "beauty", "tech"
    followers = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)    # percent, e.g. 3.5
    price_rate = Column(Float, default=0.0)         # harga per post (Rupiah)
    platform = Column(String, default="instagram")  # instagram, tiktok, youtube

    user = relationship("User", backref="influencer_profile")