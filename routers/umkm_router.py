from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from auth.jwt_handler import require_umkm
from models.user import User
from schemas.umkm_profile import UMKMProfileCreate, UMKMProfileResponse
from services.umkm_service import create_umkm_profile, get_my_umkm_profile

router = APIRouter(prefix="/umkm", tags=["UMKM Profile"])


@router.post("/profile", response_model=UMKMProfileResponse, status_code=201,
             summary="Buat profil UMKM")
def create_profile(
    data: UMKMProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    return create_umkm_profile(db, data, current_user.id)


@router.get("/profile/me", response_model=UMKMProfileResponse,
            summary="Lihat profil UMKM saya")
def my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_umkm),
):
    return get_my_umkm_profile(db, current_user.id)
