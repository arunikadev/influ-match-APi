# InfluMatch API

Sistem backend REST API yang menghubungkan **UMKM** dengan **Influencer** melalui fitur *matching otomatis* berbasis kategori, budget, dan performa influencer.

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| Framework | FastAPI (Python 3.9+) |
| ORM | SQLAlchemy |
| Database | SQLite (influmatch.db) |
| Autentikasi | JWT (python-jose + passlib/bcrypt) |
| Validasi | Pydantic v2 |
| Dokumentasi | Swagger UI (`/docs`) |
| Server | Uvicorn |

---

## How to Run

```bash
# 1. Aktifkan virtual environment
.\influenv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Akses docs: **http://localhost:8000/docs**

---

## ERD (Entity Relationship Diagram)

```
users (1) ──────────── (1) umkm_profiles
  │                            │
  │                            │ (1)
  │                            │
  │                       (N) campaigns ──── (N) match_results
  │                                                   │
  │                                                   │ (N)
  │                                                   │
  └──── (1) influencer_profiles ─────────────────────┘
```

### Relasi:
- `User` → `UMKMProfile`: One-to-One (via `user_id`)
- `User` → `InfluencerProfile`: One-to-One (via `user_id`)
- `UMKMProfile` → `Campaign`: **One-to-Many** (1 UMKM bisa punya banyak campaign)
- `Campaign` → `MatchResult`: One-to-Many
- `InfluencerProfile` → `MatchResult`: One-to-Many

---

## Role-Based Access Control

| Role | Akses |
|---|---|
| `umkm` | Kelola campaign, lihat matching influencer |
| `influencer` | Kelola profil sendiri |
| _publik_ | Lihat daftar influencer |

---

## API Endpoints

### Authentication
| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| POST | `/auth/register` | Register akun baru | ❌ |
| POST | `/auth/login` | Login, dapatkan JWT token | ❌ |

### UMKM Profile
| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| POST | `/umkm/profile` | Buat profil UMKM | ✅ UMKM |
| GET | `/umkm/profile/me` | Lihat profil saya | ✅ UMKM |

### Campaign (CRUD Lengkap)
| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| POST | `/campaign` | Buat campaign baru | ✅ UMKM |
| GET | `/campaign` | List semua campaign saya | ✅ UMKM |
| GET | `/campaign/{id}` | Detail campaign by ID | ✅ UMKM |
| PUT | `/campaign/{id}` | Update campaign | ✅ UMKM |
| DELETE | `/campaign/{id}` | Hapus campaign | ✅ UMKM |
| GET | `/campaign/{id}/matches` | Matching influencer | ✅ UMKM |

### Influencer (CRUD Lengkap)
| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| POST | `/influencer/profile` | Buat profil influencer | ✅ Influencer |
| GET | `/influencer/profile/me` | Lihat profil saya | ✅ Influencer |
| PUT | `/influencer/profile` | Update profil | ✅ Influencer |
| DELETE | `/influencer/profile` | Hapus profil | ✅ Influencer |
| GET | `/influencers` | Daftar semua influencer | ❌ Publik |

---

## Matching Engine

Sistem menghitung skor kecocokan antara campaign dan influencer:

```
Category match (niche == category_target) → +50 poin
Budget fit (price_rate ≤ budget)          → +30 poin
Engagement rate (proporsional, maks 10%)  → +0 s/d +20 poin
──────────────────────────────────────────────────────────
Total Max Score                           = 100 poin
```

Hasil diurutkan dari score **tertinggi ke terendah**.

---

## Struktur Proyek

```
2A/
├── main.py                  # Entry point FastAPI
├── config.py                # Konfigurasi (JWT secret, DB URL)
├── database.py              # Koneksi & session SQLAlchemy
├── requirements.txt         # Dependensi Python
├── README.md                # Dokumentasi proyek
├── models/
│   ├── user.py
│   ├── umkm_profile.py
│   ├── influencer_profile.py
│   ├── campaign.py
│   └── match_result.py
├── schemas/
│   ├── user_schema.py
│   ├── umkm_profile.py
│   ├── campaign_schema.py
│   ├── influencer_schema.py
│   └── match_schema.py
├── routers/
│   ├── auth_router.py
│   ├── umkm_router.py
│   ├── campaign_router.py
│   └── influencer_router.py
├── services/
│   ├── auth_service.py
│   ├── umkm_service.py
│   ├── campaign_service.py
│   ├── influencer_service.py
│   └── matching_service.py
└── auth/
    └── jwt_handler.py
```

---

## Cara Testing (Flow)

1. **Register UMKM**: `POST /auth/register` → `{"email":"...", "password":"...", "role":"umkm"}`
2. **Login**: `POST /auth/login` → copy `access_token`
3. Gunakan token di header: `Authorization: Bearer <token>`
4. **Buat profil UMKM**: `POST /umkm/profile`
5. **Buat campaign**: `POST /campaign`
6. **Register + Login Influencer** (tab/window baru)
7. **Buat profil influencer**: `POST /influencer/profile`
8. Kembali ke UMKM → **GET** `/campaign/{id}/matches` 
