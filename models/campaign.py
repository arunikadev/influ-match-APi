from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    umkm_id = Column(Integer, ForeignKey("umkm_profiles.id"), nullable=False)

    title = Column(String, nullable=False)
    category_target = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="active")  # active / closed

    created_at = Column(DateTime, default=datetime.utcnow)

    umkm = relationship("UMKMProfile", backref="campaigns")