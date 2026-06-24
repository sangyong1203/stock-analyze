from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.init_db import seed_defaults
from app.db.session import SessionLocal


def main() -> None:
    db = SessionLocal()
    try:
        seed_defaults(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
