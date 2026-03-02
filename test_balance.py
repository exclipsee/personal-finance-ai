import tempfile
import os
import json

import db
from app import app


def test_balance_with_transactions():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    db_path = tmp.name
    try:
        db.init_db(db_path)
        db.insert_transaction('2026-01-01', 'Deposit', 10.5, db_path=db_path)
        db.insert_transaction('2026-01-02', 'Coffee', -3.0, db_path=db_path)
        db.insert_transaction('2026-01-03', 'Snack', 2.0, db_path=db_path)

        client = app.test_client()
        # override environment DB path by using query param? app uses DB_PATH global; instead set env var
        # Simpler: monkeypatch DB_PATH in app module
        from importlib import reload
        import app as app_module
        app_module.DB_PATH = db_path

        resp = client.get('/balance')
        assert resp.status_code == 200
        data = resp.get_json()
        assert abs(data['balance'] - 9.5) < 1e-6
    finally:
        try:
            os.unlink(db_path)
        except Exception:
            pass


def test_balance_empty_db():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    db_path = tmp.name
    try:
        db.init_db(db_path)
        from importlib import reload
        import app as app_module
        app_module.DB_PATH = db_path
        client = app.test_client()
        resp = client.get('/balance')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['balance'] == 0.0
    finally:
        try:
            os.unlink(db_path)
        except Exception:
            pass

