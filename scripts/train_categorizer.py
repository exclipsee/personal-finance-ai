"""Train categorization model from existing labeled transactions."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db.database import SessionLocal
from ingest.categorizer import train_model


def main():
    model_path = Path("models/categorizer.joblib")
    session = SessionLocal()
    try:
        train_model(session, model_path)
        print(f"Trained model and saved to {model_path}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
