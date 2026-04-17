from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.user_schema import UserRegister, UserLogin, UserResponse, Token
from services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201,
             summary="Register akun baru (UMKM atau Influencer)")
def register(data: UserRegister, db: Session = Depends(get_db)):
    """
    Daftarkan user baru.
    - **role**: harus `umkm` atau `influencer`
    - **password**: akan di-hash otomatis
    """
    return register_user(db, data)


@router.post("/login", response_model=Token,
             summary="Login dan dapatkan JWT Token")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Login dengan email dan password.
    Akan mengembalikan **Bearer Token** yang harus disertakan di header Authorization.
    """
    return login_user(db, data.email, data.password)
