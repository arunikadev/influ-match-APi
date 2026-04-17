from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class UMKMProfile(Base):
    __tablename__ = "umkm_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    business_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    user = relationship("User", backref="umkm_profile")