from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from models.campaign import Campaign
from models.umkm_profile import UMKMProfile
from schemas.campaign_schema import CampaignCreate, CampaignUpdate


def get_umkm_profile_or_404(db: Session, user_id: int) -> UMKMProfile:
    profile = db.query(UMKMProfile).filter(UMKMProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil UMKM belum dibuat. Silakan buat profil UMKM dulu."
        )
    return profile


def create_campaign(db: Session, data: CampaignCreate, user_id: int) -> Campaign:
    profile = get_umkm_profile_or_404(db, user_id)
    
    campaign = Campaign(
        umkm_id=profile.id,
        title=data.title,
        category_target=data.category_target,
        budget=data.budget,
        description=data.description,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def get_my_campaigns(db: Session, user_id: int) -> list[Campaign]:
    profile = get_umkm_profile_or_404(db, user_id)
    return db.query(Campaign).filter(Campaign.umkm_id == profile.id).all()


def get_campaign_by_id(db: Session, campaign_id: int, user_id: int) -> Campaign:
    profile = get_umkm_profile_or_404(db, user_id)
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.umkm_id == profile.id
    ).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign tidak ditemukan"
        )
    return campaign


def update_campaign(db: Session, campaign_id: int, data: CampaignUpdate, user_id: int) -> Campaign:
    campaign = get_campaign_by_id(db, campaign_id, user_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)
    db.commit()
    db.refresh(campaign)
    return campaign


def delete_campaign(db: Session, campaign_id: int, user_id: int) -> dict:
    campaign = get_campaign_by_id(db, campaign_id, user_id)
    db.delete(campaign)
    db.commit()
    return {"message": f"Campaign '{campaign.title}' berhasil dihapus"}
