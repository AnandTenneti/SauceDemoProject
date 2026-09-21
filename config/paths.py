from pathlib import Path
from typing import Final

PROJECT_ROOT: Final = Path(__file__).resolve().parent.parent

TEST_DATA_DIR: Final = PROJECT_ROOT / "testdata"

USERS_CSV: Final = TEST_DATA_DIR / "users.csv"
USERS_JSON: Final = TEST_DATA_DIR / "users.json"
USERS_XLSX: Final = TEST_DATA_DIR/"users.xlsx"

PRODUCTS_CSV: Final = TEST_DATA_DIR/"products.csv"
PRODUCTS_JSON: Final = TEST_DATA_DIR/"products.json"
