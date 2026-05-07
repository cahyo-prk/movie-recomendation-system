from src.data_loader import DataLoader
from src.interaction import InteractionProcessor
from src.popular_recommender import PopularRecommender
from src.collaborative_recommender import (
    CollaborativeRecommender
)

class RecommendationService:

    def __init__(self):

        # load datasets
        self.users = DataLoader.load_users(
            "data/users.csv"
        )

        self.items = DataLoader.load_items(
            "data/items.csv"
        )

        self.events = DataLoader.load_events(
            "data/events.csv"
        )

        # interaction processing
        self.events = (
            InteractionProcessor.build_interactions(
                self.events
            )
        )

        # global recommender
        self.popular_model = PopularRecommender()

        self.popular_model.fit(
            self.events,
            self.items
        )

        # collaborative recommender
        self.cf_model = CollaborativeRecommender()

        self.cf_model.fit(self.events)

    def get_popular_recommendations(self, k=10):
        recommendations = (self.popular_model.recommend(k=k))
        recommendations["popularity_score"] = (recommendations["popularity_score"].round(4))
        return recommendations

    def get_user_recommendations(self,user_id,k=10):
        recommendations = (self.cf_model.recommend(user_id=user_id, k=k))

        fallback_used = False
        # fallback to popular
        if recommendations is None:
            fallback_used = True
            recommendations = (self.popular_model.recommend(k=k))

        else:
            recommendations = (recommendations.merge(self.items,on="item_id", how="left"))
            recommendations["recommendation_score"] = (recommendations[ "recommendation_score"].round(4))
            recommendations["reason"] = ("Recommended based on similar user watch patterns" )

        return {
            "fallback_used": fallback_used,
            "recommendations": recommendations
        }