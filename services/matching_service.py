from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.campaign import Campaign
from models.influencer_profile import InfluencerProfile
from schemas.match_schema import MatchResultItem, MatchResultResponse


# ── Scoring Weights ───────────────────────────────────────────────────────────
SCORE_CATEGORY_MATCH = 50
SCORE_BUDGET_FIT = 30
SCORE_ENGAGEMENT_MAX = 20  # proportional to engagement rate


def calculate_score(campaign: Campaign, influencer: InfluencerProfile) -> tuple[float, str]:
    """
    Hitung matching score antara satu campaign dan satu influencer.

    Scoring rules:
      - Category match (niche == category_target) → +50
      - Budget fit (price_rate <= budget)          → +30
      - Engagement rate (proportional, max 20)     → +0..20

    Returns:
        (score, reason_string)
    """
    score = 0.0
    reasons = []

    # 1. Category match
    if influencer.niche.lower() == campaign.category_target.lower():
        score += SCORE_CATEGORY_MATCH
        reasons.append(f"category_match:+{SCORE_CATEGORY_MATCH}")
    else:
        reasons.append("category_match:+0")

    # 2. Budget fit
    if influencer.price_rate <= campaign.budget:
        score += SCORE_BUDGET_FIT
        reasons.append(f"budget_fit:+{SCORE_BUDGET_FIT}")
    else:
        reasons.append("budget_fit:+0 (price_rate melebihi budget)")

    # 3. Engagement rate (max 20, proportional terhadap 10%)
    # engagement_rate > 10% → full 20 poin
    engagement_contribution = min(influencer.engagement_rate / 10.0, 1.0) * SCORE_ENGAGEMENT_MAX
    score += engagement_contribution
    reasons.append(f"engagement:+{engagement_contribution:.1f} ({influencer.engagement_rate}%)")

    return round(score, 2), " | ".join(reasons)


def get_campaign_matches(db: Session, campaign_id: int, user_id: int) -> MatchResultResponse:
    from models.umkm_profile import UMKMProfile

    # Pastikan campaign milik user ini
    umkm_profile = db.query(UMKMProfile).filter(UMKMProfile.user_id == user_id).first()
    if not umkm_profile:
        raise HTTPException(status_code=404, detail="Profil UMKM tidak ditemukan")

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.umkm_id == umkm_profile.id
    ).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign tidak ditemukan")

    # Ambil semua influencer
    influencers = db.query(InfluencerProfile).all()
    if not influencers:
        return MatchResultResponse(
            campaign_id=campaign.id,
            campaign_title=campaign.title,
            total_matches=0,
            results=[],
        )

    # Hitung score untuk setiap influencer
    scored = []
    for inf in influencers:
        score, reason = calculate_score(campaign, inf)
        scored.append(MatchResultItem(influencer=inf, score=score, reason=reason))

    # Sort descending by score, hanya tampilkan score > 0
    scored = [item for item in scored if item.score > 0]
    scored.sort(key=lambda x: x.score, reverse=True)

    return MatchResultResponse(
        campaign_id=campaign.id,
        campaign_title=campaign.title,
        total_matches=len(scored),
        results=scored,
    )
