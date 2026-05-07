from fastapi import FastAPI

from src.recommendation_service import (
    RecommendationService
)

app = FastAPI(
    title="Movie Recommendation System"
)

# initialize recommendation service
service = RecommendationService()


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================
# GLOBAL POPULAR
# =========================

@app.get("/popular")
def popular(k: int = 10):

    recommendations = (
        service.get_popular_recommendations(
            k=k
        )
    )

    return {
        "k": k,
        "items": recommendations.to_dict(
            orient="records"
        )
    }


# =========================
# PERSONALIZED
# =========================

@app.get("/recommendations")
def recommendations(
    user_id: str,
    k: int = 10
):

    result = (
        service.get_user_recommendations(
            user_id=user_id,
            k=k
        )
    )

    recommendations_df = result[
        "recommendations"
    ]

    return {
        "user_id": user_id,
        "k": k,
        "fallback_used": result[
            "fallback_used"
        ],
        "items": recommendations_df.to_dict(
            orient="records"
        )
    }