from src.recommendation_service import (
    RecommendationService
)

service = RecommendationService()

# popular
popular = service.get_popular_recommendations(k=10)

print("\nTop Popular Recommendations:\n")

print(popular)

# personalized
result = service.get_user_recommendations(
    user_id="u10",
    k=10
)

print("\nPersonalized Recommendations:\n")

print(result["recommendations"])

print(
    f"\nFallback Used: {result['fallback_used']}\n"
)