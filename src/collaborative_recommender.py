import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# Personalized Collaborative Filtering Recommender
# ==========================================
class CollaborativeRecommender:

    def fit(self, interactions_df):

        # Filter: Hanya ambil interaksi yang skornya minimal 1.0
        interactions_df = interactions_df[
                interactions_df["interaction_score"] >= 1.0
            ]
        
        # Buat Matriks (Tabel User vs Item)
        self.user_item_matrix = (
            interactions_df
            .pivot_table(
                index="user_id",
                columns="item_id",
                values="interaction_score",
                aggfunc="sum",
                fill_value=0
            )
        )

        # Hitung Kemiripan Antar Film (Cosine Similarity)
        # Membandingkan kolom film satu dengan kolom film lainnya
        item_similarity = cosine_similarity(
            self.user_item_matrix.T
        )
             
        # Simpan hasil kemiripan ke dalam DataFrame
        item_ids = self.user_item_matrix.columns
        self.item_similarity_df = pd.DataFrame(
            item_similarity,
            index=item_ids,
            columns=item_ids
        )

    def recommend(self, user_id, k=10):
        # Jika user tidak ada di data, batalkan
        if user_id not in self.user_item_matrix.index:
            return None

        user_vector = self.user_item_matrix.loc[user_id]

        # Ambil riwayat tontonan user
        watched_items = user_vector[user_vector > 0].index.tolist()
        recommendation_scores = {}

        # Cari film yang mirip dengan film yang sudah ditonton
        for watched_item in watched_items:
            interaction_score = user_vector[watched_item]
            similar_items = self.item_similarity_df[watched_item]

            for item_id, similarity_score in similar_items.items():
                # Lewati jika film sudah pernah ditonton
                if item_id in watched_items:
                    continue
                # Prediksi: Semakin mirip filmnya, semakin tinggi skornya
                weighted_score = (similarity_score * interaction_score)
                recommendation_scores[item_id] = (recommendation_scores.get(item_id, 0) + weighted_score)

        # Urutkan (Ranking) dari skor tertinggi
        recommendations = sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True)

        # Add hasil ke DataFrame dan Normalisasi (skala 0-1)
        recommendations = recommendations[:k]
        recommendation_df = pd.DataFrame(recommendations, columns=["item_id","recommendation_score"])
        
        # normalize scores
        max_score = recommendation_df["recommendation_score"].max()

        if max_score > 0:
            recommendation_df["recommendation_score" ] = (recommendation_df["recommendation_score"] / max_score)

        return recommendation_df