# src/insurance/data/load.py
import pandas as pd
from pathlib import Path


DATA_DIR  = Path(__file__).resolve().parent              # …/src/insurance/data
RAW_PATH  = DATA_DIR / "raw" / "premiums.xlsx"
AGE_PATH  = DATA_DIR / "raw" / "premiums_young_with_gr.xlsx"
CLEAN_DIR = DATA_DIR / "cleaned"                        
SAMPLE_DIR_REST = DATA_DIR / "sample" / "premiums_sample.xlsx"
SAMPLE_DIR_YOUNG = DATA_DIR / "sample" / "premiums_sample_young_with_gr.xlsx"

def load_raw(path: Path | str = RAW_PATH) -> pd.DataFrame:
    """Loads the raw Excel file with insurance premiums.
    Falls back to sample dataset if raw file is not available."""
    path = Path(path)
    try:
        return pd.read_excel(path)
    
    except FileNotFoundError:
        fallback_path = (SAMPLE_DIR_YOUNG if "young" in path.name.lower() else SAMPLE_DIR_REST)
    print(f"Main dataset not found (NDA). Loading sample: {fallback_path.name}")
    return pd.read_excel(fallback_path)
   
    


def save_clean(df: pd.DataFrame, filename: str = "premiums_cleaned.csv") -> None:
    '''Saves a cleaned DataFrame to src/data/cleaned/'''
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CLEAN_DIR / filename
    df.to_csv(out_path, index=False)
    print(f"✔  Saved → {out_path}")

