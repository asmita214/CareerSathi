import re
from collections import Counter
import numpy as np

STOPWORDS = set("""a an the is are was were be been being to of in on for with and or
but if then so as at by from this that these those it its their his her they he she
you your i we our us can will would should could may might must have has had do does
did not no yes also more most such into about between often typically usually generally
role skills need needed require required responsible responsibilities include including
work working career job jobs field ensure using use used help helps""".split())


def dataset_stats(chunks):
    """Real stats computed directly from the dataset — no LLM involved."""
    role_counts = Counter(c["role"] for c in chunks)

    word_counter = Counter()
    for c in chunks:
        answer_part = c["text"].split("Answer:")[-1]
        words = re.findall(r"[a-zA-Z]{3,}", answer_part.lower())
        for w in words:
            if w not in STOPWORDS:
                word_counter[w] += 1

    return role_counts, word_counter


def role_embedding_similarity(index, chunks):
    """
    Reconstructs stored vectors directly from the FAISS index (no re-encoding),
    averages them per role to get a role 'centroid', then computes cosine
    similarity between every pair of roles.
    """
    role_to_indices = {}
    for i, c in enumerate(chunks):
        role_to_indices.setdefault(c["role"], []).append(i)

    roles = sorted(role_to_indices.keys())
    centroids = []
    for role in roles:
        vecs = np.array([index.reconstruct(i) for i in role_to_indices[role]])
        centroids.append(vecs.mean(axis=0))
    centroids = np.array(centroids)

    norms = np.linalg.norm(centroids, axis=1, keepdims=True)
    normalized = centroids / norms
    similarity_matrix = normalized @ normalized.T

    return roles, similarity_matrix


def get_role_keywords(role, chunks, top_n=15):
    """Top frequent, meaningful words for a specific role's dataset entries."""
    role_chunks = [c for c in chunks if c["role"] == role]
    counter = Counter()
    for c in role_chunks:
        answer_part = c["text"].split("Answer:")[-1]
        words = re.findall(r"[a-zA-Z]{3,}", answer_part.lower())
        for w in words:
            if w not in STOPWORDS:
                counter[w] += 1
    return [w for w, _ in counter.most_common(top_n)]


def ats_match_score(resume_text, role, chunks, extra_keywords=None):
    """
    Simple algorithmic ATS-style keyword matcher — no LLM.
    Combines dataset-derived keywords with any explicit skill list (e.g. ROLE_SKILLS).
    """
    resume_lower = resume_text.lower()
    keywords = set(get_role_keywords(role, chunks, top_n=20))
    if extra_keywords:
        keywords.update([k.lower() for k in extra_keywords])

    matched = [kw for kw in keywords if kw.lower() in resume_lower]
    missing = [kw for kw in keywords if kw.lower() not in resume_lower]

    score = round(100 * len(matched) / len(keywords), 1) if keywords else 0.0
    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing),
        "total_keywords": len(keywords),
    }