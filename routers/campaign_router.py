from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from auth.jwt_handler import require_umkm
from models.user import User
from schemas.campaign_schema import CampaignCreate, CampaignUpdate, CampaignResponse
from schemas.match_schema import MatchResultResponse
from services.campaign_service import (
    create_campaign,
    get_my_campaigns,
    get_campaign_by_id,
    update_campaign,
    delete_campaign,
)
from services.matching_service import get_campaign_matches

router = APIRouter(prefix="/campaign", tags=["Campaign (UMKM only)"])


@router.post("", response_model=CampaignResponse, status_code=201,
             summary="Buat campaign baru")
def create(
    data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    """Hanya UMKM yang sudah punya profil yang bisa membuat campaign."""
    return create_campaign(db, data, current_user.id)


@router.get("", response_model=list[CampaignResponse],
            summary="Lihat semua campaign milik saya")
def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    return get_my_campaigns(db, current_user.id)


@router.get("/{campaign_id}", response_model=CampaignResponse,
            summary="Detail campaign by ID")
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    return get_campaign_by_id(db, campaign_id, current_user.id)


@router.put("/{campaign_id}", response_model=CampaignResponse,
            summary="Update campaign")
def update(
    campaign_id: int,
    data: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    """Update title, budget, category, description, atau status campaign."""
    return update_campaign(db, campaign_id, data, current_user.id)


@router.delete("/{campaign_id}", status_code=200,
               summary="Hapus campaign")
def delete(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    return delete_campaign(db, campaign_id, current_user.id)


@router.get("/{campaign_id}/matches", response_model=MatchResultResponse,
            summary="Get matching influencer untuk campaign ini")
def match_influencers(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    """
    **CORE FEATURE** — Matching Engine.

    Sistem akan menghitung score untuk setiap influencer berdasarkan:
    - **Category match** → +50 poin
    - **Budget fit** (price_rate ≤ budget) → +30 poin
    - **Engagement rate** (proporsional, max) → +20 poin

    Hasil diurutkan dari score tertinggi.
    """
    return get_campaign_matches(db, campaign_id, current_user.id)
