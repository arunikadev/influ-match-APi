from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.influencer_profile import InfluencerProfile
from schemas.influencer_schema import InfluencerProfileCreate, InfluencerProfileUpdate


def get_or_create_influencer_profile(
    db: Session, data: InfluencerProfileCreate, user_id: int
) -> InfluencerProfile:
    existing = db.query(InfluencerProfile).filter(InfluencerProfile.user_id == user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profil influencer sudah ada, gunakan PUT untuk update"
        )
    
    profile = InfluencerProfile(
        user_id=user_id,
        niche=data.niche,
        followers=data.followers,
        engagement_rate=data.engagement_rate,
        price_rate=data.price_rate,
        platform=data.platform or "instagram",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_influencer_profile(
    db: Session, data: InfluencerProfileUpdate, user_id: int
) -> InfluencerProfile:
    profile = db.query(InfluencerProfile).filter(InfluencerProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil influencer belum ada, silakan POST dulu"
        )
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile


def get_my_influencer_profile(db: Session, user_id: int) -> InfluencerProfile:
    profile = db.query(InfluencerProfile).filter(InfluencerProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil influencer belum dibuat"
        )
    return profile


def get_all_influencers(db: Session) -> list[InfluencerProfile]:
    return db.query(InfluencerProfile).all()


def delete_influencer_profile(db: Session, user_id: int) -> dict:
    profile = db.query(InfluencerProfile).filter(InfluencerProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil influencer tidak ditemukan"
        )
    db.delete(profile)
    db.commit()
    return {"message": "Profil influencer berhasil dihapus"}
