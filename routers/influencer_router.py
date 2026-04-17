from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Response

from database import get_db
from auth.jwt_handler import require_influencer
from models.user import User
from schemas.influencer_schema import (
    InfluencerProfileCreate,
    InfluencerProfileUpdate,
    InfluencerProfileResponse,
)
from services.influencer_service import (
    get_or_create_influencer_profile,
    update_influencer_profile,
    get_my_influencer_profile,
    get_all_influencers,
    delete_influencer_profile,
)

router = APIRouter(prefix="/influencer", tags=["📱 Influencer"])


@router.post("/profile", response_model=InfluencerProfileResponse, status_code=201,
             summary="Buat profil influencer (pertama kali)")
def create_profile(
    data: InfluencerProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_influencer),
):
    return get_or_create_influencer_profile(db, data, current_user.id)


@router.get("/profile/me", response_model=InfluencerProfileResponse,
            summary="Lihat profil saya")
def my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_influencer),
):
    return get_my_influencer_profile(db, current_user.id)


@router.put("/profile", response_model=InfluencerProfileResponse,
            summary="Update profil influencer")
def update_profile(
    data: InfluencerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_influencer),
):
    return update_influencer_profile(db, data, current_user.id)


@router.delete("/profile", status_code=200,
               summary="Hapus profil influencer")
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_influencer),
):
    return delete_influencer_profile(db, current_user.id)


@router.get("s", response_model=list[InfluencerProfileResponse],
            summary="Lihat semua influencer (publik)")
def list_influencers(db: Session = Depends(get_db)):
    """Endpoint publik — tidak perlu login untuk melihat daftar influencer."""
    return get_all_influencers(db)
