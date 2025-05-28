from __future__ import annotations
import pandas as pd
from pathlib import Path

DATA_DIR  = Path(__file__).resolve().parent              # …/src/insurance/data
SPLITTED_DIR = DATA_DIR / "splitted"
SPLITTED_DIR.mkdir(parents=True, exist_ok=True) 

def segment_by_age(df: pd.DataFrame, age_cutoff: int = 25) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the dataset into two groups based on the `age_cutoff`.
    Saves both groups as Excel files in the cleaned/ folder.

    Parameters:
    - df: Full cleaned DataFrame (after preprocessing)
    - age_cutoff: Age threshold to separate young vs rest

    Returns:
    - Tuple of (df_young, df_rest)
    """
    df_young = df[df["age"] <= age_cutoff].copy()
    df_rest = df[df["age"] >  age_cutoff].copy()

    df_young.to_excel(SPLITTED_DIR / f"premiums_young.xlsx", index=False)
    df_rest.to_excel(SPLITTED_DIR / f"premiums_adult.xlsx", index=False)

    print(f"✔ Saved {df_young.shape[0]} rows → premiums_young.xlsx")
    print(f"✔ Saved {df_rest.shape[0]} rows → premiums_adult.xlsx")

    return df_young, df_rest