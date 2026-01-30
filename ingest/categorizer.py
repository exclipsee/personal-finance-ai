"""Categorization functionality moved to an optional extras package.

This repository keeps a minimal stub to avoid shipping heavy dependencies.
If you need categorization, extract `ingest/categorizer.py` into a separate
package or re-enable it and install `scikit-learn` and `joblib`.
"""

from __future__ import annotations

def train_model(*args, **kwargs):
    raise RuntimeError("Categorization has been offloaded. See CONTRIBUTING.md or create an 'extras' package to re-enable.")


def apply_predictions(*args, **kwargs):
    raise RuntimeError("Categorization has been offloaded. See CONTRIBUTING.md or create an 'extras' package to re-enable.")
