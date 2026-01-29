"""Embeddings and simple vector store for transactions.

Supports OpenAI embeddings when `OPENAI_API_KEY` is set; otherwise falls
back to TF-IDF vectors. Uses `sklearn.neighbors.NearestNeighbors` as a
lightweight local vector store and persists artifacts under `models/`.
"""
from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import List, Tuple

import numpy as np
import joblib

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except Exception:
    _OPENAI_AVAILABLE = False

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

logger = logging.getLogger(__name__)


def _collect_texts(session) -> Tuple[List[int], List[str]]:
    from db.models import Transaction

    ids = []
    texts = []
    for t in session.query(Transaction).order_by(Transaction.id):
        ids.append(t.id)
        cat = t.category or ""
        texts.append(f"{t.description or ''} | {cat} | {t.amount}")
    return ids, texts


def _openai_embed(texts: List[str]) -> List[List[float]]:
    # Use the OpenAI embeddings API if available.
    if not _OPENAI_AVAILABLE or not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OpenAI embedding provider not available or API key missing")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # prefer small embedding model; adjust as needed
    model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    resp = client.embeddings.create(input=texts, model=model)
    return [e.embedding for e in resp.data]


def build_embeddings(session, out_dir: str | Path = "models", provider: str = "auto") -> Path:
    """Build embeddings for all transactions and persist a vector store.

    provider: 'auto' -> tries OpenAI then falls back to 'tfidf'
    Returns path to saved artifact (joblib) containing {'ids', 'vectors', 'nn'}
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ids, texts = _collect_texts(session)

    if provider == "auto":
        if _OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        else:
            provider = "tfidf"

    if provider == "openai":
        try:
            vectors = _openai_embed(texts)
            vectors = np.array(vectors, dtype=float)
        except Exception as e:
            logger.warning("OpenAI embedding failed: %s, falling back to TF-IDF", e)
            provider = "tfidf"

    if provider == "tfidf":
        vec = TfidfVectorizer(max_features=20_000, ngram_range=(1, 2))
        vectors = vec.fit_transform(texts).toarray()
        # persist vectorizer so queries can be embedded consistently
        joblib.dump(vec, out_dir / "tfidf_vectorizer.joblib")

    # Build nearest-neighbors index
    nn = NearestNeighbors(n_neighbors=10, algorithm="auto", metric="cosine")
    nn.fit(vectors)

    artifact = {
        "ids": ids,
        "vectors": vectors,
        "nn": nn,
        "provider": provider,
    }
    path = out_dir / "embeddings.joblib"
    joblib.dump(artifact, path)
    logger.info("Saved embeddings artifact to %s (provider=%s)", path, provider)
    return path


def _load_artifact(path: str | Path):
    return joblib.load(str(path))


def _embed_query(text: str, artifact_dir: str | Path = "models") -> np.ndarray:
    artifact_dir = Path(artifact_dir)
    provider = None
    vec = None
    if (artifact_dir / "embeddings.joblib").exists():
        a = joblib.load(artifact_dir / "embeddings.joblib")
        provider = a.get("provider")

    if provider == "openai" and _OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        v = _openai_embed([text])[0]
        return np.array(v, dtype=float)

    # TF-IDF fallback
    vec = joblib.load(artifact_dir / "tfidf_vectorizer.joblib")
    return vec.transform([text]).toarray()[0]


def query(text: str, artifact_path: str | Path = "models/embeddings.joblib", top_k: int = 10) -> List[Tuple[int, float]]:
    """Return list of (transaction_id, distance) for top_k nearest transactions."""
    artifact = _load_artifact(artifact_path)
    ids = artifact["ids"]
    vectors = artifact["vectors"]
    nn = artifact["nn"]

    qv = _embed_query(text, Path(artifact_path).parent)
    dists, idxs = nn.kneighbors([qv], n_neighbors=min(top_k, len(ids)))
    results: List[Tuple[int, float]] = []
    for dist, idx in zip(dists[0], idxs[0]):
        results.append((ids[int(idx)], float(dist)))
    return results
