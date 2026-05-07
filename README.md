# Movie Recommendation System

## Overview

This project is a Movie Recommendation System built using:

* Collaborative Filtering
* Popularity-Based Recommendation
* Implicit Feedback Modeling
* FastAPI

The system provides:

1. Global Popular Recommendations
2. Personalized Recommendations
3. Cold-Start Fallback Handling

---

# Project Objectives

The recommendation system has two main objectives:

| Objective                   | Description                              |
| --------------------------- | ---------------------------------------- |
| Global Recommendation       | Recommend globally trending content      |
| Personalized Recommendation | Recommend content based on user behavior |

---

# Dataset

The project uses 3 CSV files.

---

## 1. users.csv

Contains user profile information.

| Column  | Description            |
| ------- | ---------------------- |
| user_id | Unique user identifier |
| age     | User age               |
| gender  | User gender            |
| region  | User region            |

Example:

| user_id | age | gender | region  |
| ------- | --- | ------ | ------- |
| u1      | 25  | male   | jakarta |

---

## 2. items.csv

Contains movie/content metadata.

| Column       | Description               |
| ------------ | ------------------------- |
| item_id      | Unique content identifier |
| title        | Movie/show title          |
| content_type | movie / series / tv       |
| genre        | Content genre             |

Example:

| item_id | title  | genre |
| ------- | ------ | ----- |
| i10     | Naruto | anime |

---

## 3. events.csv

Contains user interaction history.

| Column        | Description           |
| ------------- | --------------------- |
| user_id       | User identifier       |
| item_id       | Content identifier    |
| event_type    | Interaction type      |
| watch_seconds | Watch duration        |
| timestamp     | Interaction timestamp |

Example:

| user_id | item_id | event_type | watch_seconds |
| ------- | ------- | ---------- | ------------- |
| u1      | i10     | like       | 1200          |

---

# Recommendation System Approach

The project uses:

# Hybrid Recommendation Approach

Combining:

1. Collaborative Filtering
2. Popularity-Based Recommendation
3. Rule-Based Interaction Weighting

---

# Why Collaborative Filtering?

Collaborative filtering is used because:

* recommendation is based on user behavior
* users with similar viewing patterns tend to like similar content
* suitable for implicit feedback datasets
* scalable and commonly used in recommender systems

---

# Why Popular Recommendation?

Popularity recommendation is used for:

* cold-start users
* fallback recommendations
* globally trending content

---

# System Architecture

```text
movie-recommendation-system/
│
├── data/
│   ├── users.csv
│   ├── items.csv
│   └── events.csv
│
├── src/
│   ├── data_loader.py
│   ├── interaction.py
│   ├── popular_recommender.py
│   ├── collaborative_recommender.py
│   ├── recommendation_service.py
│   └── api.py
│
├── main.py
└── requirements.txt
```

---

# End-to-End System Flow

```text
CSV Data
   ↓
Data Loading
   ↓
Interaction Processing
   ↓
User-Item Matrix
   ↓
Collaborative Filtering
   ↓
Recommendation Ranking
   ↓
Fallback Handling
   ↓
FastAPI Response
```

---

# 1. data_loader.py

## Purpose

Responsible for:

* loading CSV files
* validating schema
* preventing missing columns

---

## Key Logic

```python
REQUIRED_EVENTS_COLUMNS = [
    "user_id",
    "item_id",
    "event_type",
    "watch_seconds",
    "timestamp"
]
```

The system validates required columns before processing data.

---

## Why Validation Is Important

Recommendation systems depend heavily on:

* consistent schema
* valid columns
* structured interaction data

Without validation:

* recommendation pipeline may fail
* similarity matrix becomes invalid

---

# 2. interaction.py

## Purpose

Transforms raw user interaction into:

# interaction_score

This is the most important feature in the recommendation system.

---

# Why Interaction Engineering Is Needed

Raw interaction data cannot be used directly because:

| Problem                 | Explanation                    |
| ----------------------- | ------------------------------ |
| watch_seconds too large | extreme values dominate        |
| different event types   | different engagement meaning   |
| old interactions        | should become weaker over time |

---

# Event Weighting

Different interaction events represent different engagement strength.

```python
EVENT_WEIGHTS = {
    "skip": 0.2,
    "pause": 0.5,
    "play": 1.0,
    "complete": 1.5,
    "like": 2.0,
    "save": 2.0
}
```

---

# Event Meaning

| Event     | Meaning                  |
| --------- | ------------------------ |
| skip      | weak interest            |
| pause     | partial engagement       |
| play      | normal interaction       |
| complete  | strong engagement        |
| like/save | explicit positive intent |

---

# Interaction Formula

The system calculates:

interaction_score = EventWeight × log(1 + watch_seconds) × RecencyWeight

---

# Formula Breakdown

## A. Event Weight

Represents:

# user intent strength

Example:

| Event | Weight |
| ----- | ------ |
| like  | 2.0    |
| skip  | 0.2    |

Meaning:

* liked content influences recommendations more strongly
* skipped content has very weak influence

---

## B. log(1 + watch_seconds)

Used for:

# watch duration normalization

---

# Why Log Scaling?

Raw watch duration may contain extreme values.

Example:

| watch_seconds |
| ------------- |
| 10            |
| 10000         |

Without scaling:

* long-watch users dominate recommendations.

---

# Example Transformation

| watch_seconds | log value |
| ------------- | --------- |
| 10            | 2.39      |
| 100           | 4.61      |
| 1000          | 6.90      |

The values become smoother and more stable.

---

## C. Recency Weight

The system also applies:

# recency decay

Formula:

RecencyWeight = exp(-days_ago / 30)

---

# Why Recency Weight?

Because user preferences change over time.

Recent interactions should influence recommendations more strongly.

---

# Example

| Interaction | Weight |
| ----------- | ------ |
| yesterday   | high   |
| 90 days ago | low    |

---

# Final Interaction Score Example

| Event | Watch | Recency | Final Score |
| ----- | ----- | ------- | ----------- |
| like  | 1000  | recent  | high        |
| skip  | 50    | old     | low         |

---

# 3. collaborative_recommender.py

## Purpose

Main engine for:

# personalized recommendation

---

# Step 1 — Filter Weak Interactions

```python
interactions_df = interactions_df[
    interactions_df["interaction_score"] >= 1.0
]
```

---

# Why?

Removes:

* noisy interactions
* accidental clicks
* weak engagement

This improves recommendation quality.

---

# Step 2 — Build User-Item Matrix

```python
pivot_table(
    index="user_id",
    columns="item_id",
    values="interaction_score"
)
```

---

# Result Example

| user | Naruto | Frozen | Interstellar |
| ---- | ------ | ------ | ------------ |
| U1   | 12.5   | 2.0    | 8.1          |
| U2   | 11.0   | 0      | 7.2          |

---

# Matrix Meaning

| Component | Meaning              |
| --------- | -------------------- |
| rows      | users                |
| columns   | movies/items         |
| values    | interaction strength |

---

# Why This Matrix Is Important

Collaborative filtering learns from:

# user behavioral patterns

---

# Step 3 — Cosine Similarity

```python
cosine_similarity(
    self.user_item_matrix.T
)
```

---

# Why .T (Transpose)?

The original matrix is:

# user-item

But collaborative filtering compares:

# item-item similarity

So the matrix is transposed into:

# item-user

---

# Why Cosine Similarity?

Because:

* suitable for sparse matrix
* efficient
* common recommender system approach
* measures behavioral similarity

---

# Example

If many users watch:

* Naruto
* Jujutsu Kaisen

together,
then:

# similarity becomes high

---

# Step 4 — Recommendation Scoring

Formula:

RecommendationScore = Similarity × InteractionStrength

---

# Example

| Item      | Similarity |
| --------- | ---------- |
| Blue Lock | 0.9        |

| User Interaction With Naruto |
| ---------------------------- |
| 12                           |

Final Score:

0.9 × 12 = 10.8

---

# Meaning

Because the user strongly likes Naruto,
related anime recommendations become stronger.

---

# Step 5 — Exclude Watched Content

```python
if item_id in watched_items:
    continue
```

---

# Why?

Recommending already watched content is bad user experience.

---

# Step 6 — Score Normalization

```python
recommendation_score / max_score
```

---

# Why Normalize?

To make recommendation scores:

* easier to interpret
* frontend friendly
* consistent between users

---

# Example

| Before | After |
| ------ | ----- |
| 14.2   | 1.0   |
| 12.1   | 0.85  |

---

# 4. popular_recommender.py

## Purpose

Responsible for:

# global popular recommendations

---

# Why Popular Recommendation Is Needed

Collaborative filtering cannot personalize:

* new users
* users without history

This is called:

# cold-start problem

---

# Popularity Formula

Popularity =
0.7 × TotalInteractionScore
+
0.3 × UniqueUserCount

---

# Why Combine Two Signals?

Because the system should consider:

| Signal            | Meaning              |
| ----------------- | -------------------- |
| interaction score | engagement quality   |
| unique users      | popularity frequency |

---

# Example

| Movie        | Interaction | Users |
| ------------ | ----------- | ----- |
| Naruto       | high        | many  |
| Random Movie | high        | 1     |

Naruto becomes more globally popular.

---

# 5. recommendation_service.py

## Purpose

Acts as:

# orchestration layer

---

# Responsibilities

* initialize recommenders
* centralize business logic
* handle fallback logic
* prepare API-ready outputs

---

# Why Service Layer Is Important

Keeps:

* API clean
* recommendation logic reusable
* architecture modular

---

# Fallback Logic

```python
if (
    recommendations is None or
    recommendations.empty
):
```

---

# Why?

Some users may:

* not exist
* have too few interactions
* generate no recommendations

The system then falls back to:

# popular recommendations

---

# 6. api.py

## Purpose

Expose recommendation system through:

# FastAPI endpoints

---

# Why FastAPI?

Because:

* lightweight
* fast
* easy API documentation
* suitable for ML/recommendation services

---

# Endpoints

## Health Check

```http
GET /health
```

Used for:

* service monitoring
* deployment health checking

---

## Global Recommendation

```http
GET /popular?k=10
```

Returns:

* globally popular content

---

## Personalized Recommendation

```http
GET /recommendations?user_id=u10&k=10
```

Returns:

* personalized recommendations
* fallback information

---

# Example API Response

```json
{
  "user_id": "u10",
  "fallback_used": false,
  "items": [
    {
      "title": "Blue Lock",
      "recommendation_score": 0.91
    }
  ]
}
```

---

# Final Recommendation Flow

```text
User Events
    ↓
Interaction Engineering
    ↓
Behavioral Representation
    ↓
Collaborative Filtering
    ↓
Recommendation Ranking
    ↓
Fallback Handling
    ↓
API Response
```

---

# Final Conclusion

This project implements a:

# behavior-driven recommendation system

using:

* implicit feedback modeling
* collaborative filtering
* cosine similarity
* interaction engineering
* recency weighting
* popularity fallback

The system generates:

* personalized movie recommendations
* globally trending recommendations

with a modular and API-ready architecture.
