# src/insurance/data/load.py
import pandas as pd
from pathlib import Path


DATA_DIR  = Path(__file__).resolve().parent              # …/src/insurance/data
RAW_PATH  = DATA_DIR / "raw" / "premiums.xlsx"
CLEAN_DIR = DATA_DIR / "cleaned"                        

def load_raw(path: Path | str = RAW_PATH) -> pd.DataFrame:
    """Loads the raw Excel file with insurance premiums."""
    return pd.read_excel(path)


def save_clean(df: pd.DataFrame, filename: str = "premiums_cleaned.csv") -> None:
    '''Saves a cleaned DataFrame to src/data/cleaned/'''
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CLEAN_DIR / filename
    df.to_csv(out_path, index=False)
    print(f"✔  Saved → {out_path}")

