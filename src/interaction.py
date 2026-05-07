import numpy as np
import pandas as pd

# ==========================================
# 1. STANDAR PENILAIAN (BOBOT)
# ==========================================

EVENT_WEIGHTS = {
    "skip": 0.2, # Tidak suka
    "pause": 0.5, # Tertarik tapi ragu
    "play": 1.0, # Nonton biasa
    "complete": 2.0, # Suka banget
    "like": 2.0, # Suka banget
    "save": 2.0 # Suka banget
}

# ==========================================
# 2. PENGOLAH SKOR INTERAKSI
# ==========================================
class InteractionProcessor:

    @staticmethod
    def build_interactions(events_df: pd.DataFrame):

        df = events_df.copy()

        # A. Konversi Waktu
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        latest_timestamp = df["timestamp"].max()

        # B. Hitung Faktor "Kebaruan" (Recency)
        # Semakin lama ditonton, skor makin kecil (basi)
        df["days_ago"] = (latest_timestamp - df["timestamp"]).dt.days
        df["recency_weight"] = np.exp(-df["days_ago"] / 30)

        # C. Ambil Bobot Aksi dari kamus EVENT_WEIGHTS
        df["event_weight"] = df["event_type"].map(EVENT_WEIGHTS).fillna(1.0)

        # D. Rumus Final Skor Interaksi
        # Skor = Bobot Aksi * Logaritma(Durasi) * Bobot Waktu
        df["interaction_score"] = (
            df["event_weight"] *
            np.log1p(df["watch_seconds"]) *
            df["recency_weight"]
        )
        return df