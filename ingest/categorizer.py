"""Simple categorization ML: TF-IDF + LogisticRegression classifier.

Functions:
- train_model(session, model_path): train on existing transactions with categories
- predict_for_unlabeled(session, model_path, limit): predict and return suggested categories
- apply_predictions(session, model_path, limit): update DB transaction.category with predictions
"""
from __future__ import annotations

import logging
from typing import List
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


def _gather_training(session):
    from db.models import Transaction

    q = session.query(Transaction).filter(Transaction.category != None)
    texts = []
    labels = []
    for t in q:
        text = f"{t.description or ''}"
        texts.append(text)
        labels.append(t.category)
    return texts, labels


def train_model(session, model_path: str | Path):
    texts, labels = _gather_training(session)
    if not texts:
        raise RuntimeError("No labeled transactions found to train on.")

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=10_000, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000)),
    ])

    pipeline.fit(texts, labels)
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, str(model_path))
    logger.info("Saved categorizer model to %s", model_path)
    return model_path


def _load_model(model_path: str | Path) -> Pipeline:
    return joblib.load(str(model_path))


def predict_for_unlabeled(session, model_path: str | Path, limit: int = 100) -> List[tuple]:
    from db.models import Transaction

    model = _load_model(model_path)
    q = session.query(Transaction).filter((Transaction.category == None) | (Transaction.category == ""))
    q = q.order_by(Transaction.date.desc()).limit(limit)
    results = []
    texts = []
    txs = []
    for t in q:
        texts.append(t.description or "")
        txs.append(t)

    if not texts:
        return []

    preds = model.predict(texts)
    for tx, p in zip(txs, preds):
        results.append((tx.id, tx.description, p))
    return results


def apply_predictions(session, model_path: str | Path, limit: int = 100) -> int:
    from db.models import Transaction

    model = _load_model(model_path)
    q = session.query(Transaction).filter((Transaction.category == None) | (Transaction.category == ""))
    q = q.order_by(Transaction.date.desc()).limit(limit)
    count = 0
    for t in q:
        pred = model.predict([t.description or ""])[0]
        t.category = pred
        count += 1
    session.commit()
    return count
