from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.umkm_profile import UMKMProfile
from schemas.umkm_profile import UMKMProfileCreate


def create_umkm_profile(db: Session, data: UMKMProfileCreate, user_id: int) -> UMKMProfile:
    existing = db.query(UMKMProfile).filter(UMKMProfile.user_id == user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profil UMKM sudah ada"
        )
    
    profile = UMKMProfile(
        user_id=user_id,
        business_name=data.business_name,
        category=data.category,
        description=data.description,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_my_umkm_profile(db: Session, user_id: int) -> UMKMProfile:
    profile = db.query(UMKMProfile).filter(UMKMProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil UMKM belum dibuat"
        )
    return profile
