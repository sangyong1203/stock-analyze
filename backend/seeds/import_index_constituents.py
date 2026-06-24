import argparse
from datetime import date
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.domains.collection.schemas import IndexConstituentImportRequest
from app.domains.collection.service import import_index_constituents


def main() -> None:
    parser = argparse.ArgumentParser(description="Import KODEX index constituents from CSV/XLS/XLSX")
    parser.add_argument("--file", required=True, help="CSV/XLSX file path")
    parser.add_argument("--index-code", required=True, choices=["KODEX_200", "KODEX_KOSDAQ_150", "KODEX_KOSDAQ150"])
    parser.add_argument("--index-name", required=True)
    parser.add_argument("--effective-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--tracking-index", default=None)
    parser.add_argument("--source", default="manual")
    args = parser.parse_args()

    payload = IndexConstituentImportRequest(
        file_path=args.file,
        index_code=args.index_code,
        index_name=args.index_name,
        tracking_index=args.tracking_index,
        effective_date=date.fromisoformat(args.effective_date),
        source=args.source,
    )
    db = SessionLocal()
    try:
        result = import_index_constituents(db, payload)
        print(result.model_dump())
    finally:
        db.close()


if __name__ == "__main__":
    main()
