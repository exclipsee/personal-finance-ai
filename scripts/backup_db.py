"""Create an encrypted backup of the local SQLite DB (`./finance.db`).

The script uses a symmetric key from `DB_BACKUP_KEY` env var (base64 urlsafe bytes)
compatible with `cryptography.fernet.Fernet`. If the key is not set the script
prints instructions to generate one.
"""
from __future__ import annotations

from pathlib import Path
import os
import sys
import base64

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from cryptography.fernet import Fernet
except Exception:
    Fernet = None  # type: ignore


def backup_db(db_path: Path, out_dir: Path, key: str | None) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if not db_path.exists():
        raise FileNotFoundError(f"DB not found: {db_path}")

    if not key:
        # print how to generate a key
        print("DB_BACKUP_KEY not set. Generate one with:\n  python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"")
        raise RuntimeError("Missing DB_BACKUP_KEY")

    if Fernet is None:
        raise RuntimeError("cryptography is not installed; install it with pip install cryptography")

    # ensure key is valid base64 urlsafe
    try:
        key_bytes = key.encode() if isinstance(key, str) else key
        # validate by constructing Fernet
        f = Fernet(key_bytes)
    except Exception as e:
        raise RuntimeError("Invalid DB_BACKUP_KEY; must be urlsafe-base64 32-byte key") from e

    data = db_path.read_bytes()
    token = f.encrypt(data)
    out_path = out_dir / f"{db_path.name}.enc"
    out_path.write_bytes(token)
    return out_path


def main():
    db_path = Path(os.getenv("DATABASE_FILE", "./finance.db"))
    out_dir = Path(os.getenv("BACKUP_DIR", "backups"))
    key = os.getenv("DB_BACKUP_KEY")
    path = backup_db(db_path, out_dir, key)
    print(f"Wrote encrypted backup to {path}")


if __name__ == "__main__":
    main()
