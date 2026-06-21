"""
Cosine similarity-based job recommender using TF-IDF.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def build_user_query(profile):
    """Build a weighted text query from the user's profile."""
    parts = []
    # Repeat skills 3x to boost their weight
    skills = " ".join(profile.skills_list())
    parts.extend([skills] * 3)
    # Roles 2x
    roles = " ".join(profile.roles_list())
    parts.extend([roles] * 2)
    # Location once
    if profile.preferred_locations:
        parts.append(profile.preferred_locations)
    return " ".join(parts)


def rank_jobs(profile, job_postings):
    """
    Rank job postings by cosine similarity to user profile.
    Returns list of (job, score) tuples sorted descending.
    """
    if not job_postings:
        return []

    user_query = build_user_query(profile)
    job_texts = [job.searchable_text() for job in job_postings]

    # Fit TF-IDF on jobs + user query together
    corpus = job_texts + [user_query]
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # User vector is the last row
    user_vector = tfidf_matrix[-1]
    job_vectors = tfidf_matrix[:-1]

    scores = cosine_similarity(user_vector, job_vectors).flatten()

    ranked = sorted(
        zip(job_postings, scores.tolist()),
        key=lambda x: x[1],
        reverse=True,
    )
    return ranked
