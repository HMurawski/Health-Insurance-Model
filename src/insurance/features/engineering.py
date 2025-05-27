"""
Low-level cleaning utilities and the prepare_data() meta-function.
This module contains **no sklearn code** - just pure pandas operations.
"""
from __future__ import annotations
import pandas as pd

# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #
def clean_age(val: int | str) -> int:
    """
    Removes the first digit from age values with >2 digits (data-entry glitch).

    Examples
    --------
    185 → 85 , 99 → 99
    """
    val_str = str(val)
    if len(val_str) > 2:
        return int(val_str[1:])
    return int(val)

def get_salary_bounds(col: pd.Series) -> tuple[float, float]:
    """IQR-based bounds for outlier detection (25 % - 90 % quantiles)."""
    q1, q3 = col.quantile([0.25, 0.90])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


# ------------------------------------------------------------------ #
# Main cleaning routine
# ------------------------------------------------------------------ #
def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline that:
    1. Standardises column names
    2. Drops NAs / duplicates
    3. Fixes basic data-entry errors
    4. Removes salary outliers
    5. Normalises smoking-status wording
    """
    df = df.copy()
    df.columns = df.columns.str.replace(" ", "_").str.lower()

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Fix negative dependants
    if "number_of_dependants" in df.columns:
        df["number_of_dependants"] = df["number_of_dependants"].abs()

    # Clean age & filter adults
    if "age" in df.columns:
        df["age"] = df["age"].apply(clean_age)
        df = df[df["age"] >= 18]

    # Remove extreme incomes
    if "income_lakhs" in df.columns:
        low, high = get_salary_bounds(df["income_lakhs"])
        df = df[df["income_lakhs"] < high]

    # Standardise smoking status
    if "smoking_status" in df.columns:
        df["smoking_status"] = df["smoking_status"].replace(
            {
                "Smoking=0": "No Smoking",
                "Does Not Smoke": "No Smoking",
                "Not Smoking": "No Smoking",
            }
        )

    return df.reset_index(drop=True)
