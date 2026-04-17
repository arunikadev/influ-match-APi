from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from models.umkm_profile import UMKMProfile
from models.influencer_profile import InfluencerProfile
from schemas.user_schema import UserRegister
from auth.jwt_handler import hash_password, verify_password, create_access_token


def register_user(db: Session, data: UserRegister) -> User:
    # Cek email sudah dipakai
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar"
        )
    
    user = User(
        email=data.email,
        password=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah"
        )
    
    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id,
    }
