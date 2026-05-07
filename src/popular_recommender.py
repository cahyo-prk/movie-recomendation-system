import pandas as pd

# ==========================================
# REKOMENDASI TREN (GLOBAL)
# ==========================================

class PopularRecommender:

    def fit(self, interactions_df, items_df):
        # Hitung total suara dan jumlah orang yang nonton
        popularity_df = (
            interactions_df
            .groupby("item_id")
            .agg({
                "interaction_score": "sum",
                "user_id": "count"
            })
            .reset_index()
        )
        
        popularity_df.columns = ["item_id", "total_interaction_score", "event_count"]

        # Rumus gabungan: 70% Kualitas, 30% Viralitas
        popularity_df["popularity_score"] = (
            0.7 * popularity_df["total_interaction_score"] +
            0.3 * popularity_df["event_count"]
        )

        # merge movie info
        popularity_df = popularity_df.merge(items_df, on="item_id", how="left")
        self.popularity_df = popularity_df.sort_values("popularity_score", ascending=False)

    def recommend(self, k=10):
        # Berikan daftar teratas untuk semua orang
        recommendations = self.popularity_df.head(k).copy()
        recommendations["reason"] = ("Trending globally based on user engagement")

        return recommendations[[
            "item_id",
            "title",
            "genre",
            "content_type",
            "popularity_score",
            "reason"
        ]]