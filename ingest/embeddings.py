"""Embeddings functionality moved to an optional extras package.

This repository keeps a minimal stub to avoid shipping heavy dependencies.
If you need embeddings, consider extracting `ingest/embeddings.py` into a
separate package or re-enable the implementation and install the required
dependencies (`scikit-learn`, `numpy`, `joblib` or `openai`).
"""

from __future__ import annotations

def build_embeddings(*args, **kwargs):
    raise RuntimeError("Embeddings functionality has been offloaded. See CONTRIBUTING.md or create an 'extras' package to re-enable.")


def query(*args, **kwargs):
    raise RuntimeError("Embeddings functionality has been offloaded. See CONTRIBUTING.md or create an 'extras' package to re-enable.")
