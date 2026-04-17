from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import engine
import models  # import semua model agar SQLAlchemy registrasikan tabel
from database import Base

from routers.auth_router import router as auth_router
from routers.campaign_router import router as campaign_router
from routers.influencer_router import router as influencer_router
from routers.umkm_router import router as umkm_router

# ── Buat semua tabel jika belum ada ──────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Inisialisasi App ──────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## 🎯 InfluMatch API

Sistem backend REST API yang menghubungkan **UMKM** dengan **Influencer** melalui fitur
**matching otomatis** berbasis kategori, budget, dan performa influencer.

---

### 🔐 Authentication
Semua endpoint yang dilindungi memerlukan **Bearer Token** dari endpoint `/auth/login`.

### 👥 Role
- **UMKM**: bisa membuat campaign dan melihat matching influencer
- **Influencer**: bisa membuat/update profil

### 🧠 Matching Engine
Sistem memberikan **score** untuk setiap influencer berdasarkan:
- Category match → **+50**
- Budget fit → **+30**  
- Engagement rate → **+0–20**
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include Routers ───────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(umkm_router)
app.include_router(campaign_router)
app.include_router(influencer_router)


# ── Root Endpoint ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running ✅",
    }