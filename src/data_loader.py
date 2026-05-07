import pandas as pd


REQUIRED_USERS_COLUMNS = [
    "user_id",
    "age",
    "gender",
    "region"
]

REQUIRED_ITEMS_COLUMNS = [
    "item_id",
    "title",
    "content_type",
    "genre"
]

REQUIRED_EVENTS_COLUMNS = [
    "user_id",
    "item_id",
    "event_type",
    "watch_seconds",
    "timestamp"
]


class DataLoader:

    @staticmethod
    def validate_columns(df, required_columns, file_name):

        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing columns in {file_name}: {missing_columns}"
            )

    @staticmethod
    def load_users(path):

        df = pd.read_csv(path)

        DataLoader.validate_columns(
            df,
            REQUIRED_USERS_COLUMNS,
            "users.csv"
        )

        return df

    @staticmethod
    def load_items(path):

        df = pd.read_csv(path)

        DataLoader.validate_columns(
            df,
            REQUIRED_ITEMS_COLUMNS,
            "items.csv"
        )

        return df

    @staticmethod
    def load_events(path):

        df = pd.read_csv(path)

        DataLoader.validate_columns(
            df,
            REQUIRED_EVENTS_COLUMNS,
            "events.csv"
        )

        return df