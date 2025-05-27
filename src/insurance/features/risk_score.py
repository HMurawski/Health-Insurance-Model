"""
Adds disease  ➜  risk-score feature.
"""
from __future__ import annotations
import pandas as pd

_RISK_SCORES = {
    "diabetes": 6,
    "heart disease": 8,
    "high blood pressure": 6,
    "thyroid": 5,
    "no disease": 0,
    "none": 0,
}

def add_normalized_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """Splits medical history and adds a 0-1 normalised risk score column."""
    df = df.copy()

    # Split `medical_history`
    df[["disease1", "disease2"]] = (
        df["medical_history"]
        .str.split(" & ", expand=True)
        .apply(lambda s: s.str.lower())
    )

    df.fillna("none", inplace=True)

    # Map to numeric risk
    df["total_risk_score"] = 0
    for col in ["disease1", "disease2"]:
        df["total_risk_score"] += df[col].map(_RISK_SCORES)

    rng = df["total_risk_score"]
    df["normalized_risk_score"] = (rng - rng.min()) / (rng.max() - rng.min())

    return df
