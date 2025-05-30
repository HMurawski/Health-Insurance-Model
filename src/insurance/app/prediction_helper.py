"""
Single entry point: predict(features_dict)  →  (premium, est_perc_error)

• automatically loads the latest *.joblib models from app/artifacts/
• selects the "young" model (≤25 years) or "rest"
• maps input data to the exact structure expected by the pipelines (no manual scaling!)
"""

from __future__ import annotations
from pathlib import Path
import joblib, pandas as pd, numpy as np

# ──────────────────────────────────── stałe
ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
INSURANCE_MAP = {"Bronze": 1, "Silver": 2, "Gold": 3}
KPI_THRESHOLD = 0.10                        # 10 % KPI
_CV_MAE = {"young": 250.38, "rest": 256.43}       # cross-validated MAE by age group (data in notebooks)

_RISK = {
    "diabetes": 6, "heart disease": 8, "high blood pressure": 6,
    "thyroid": 5, "no disease": 0, "none": 0,
}

# ──────────────────────────────────── Load latest model files
def _latest(pattern: str) -> Path:
    """Returns the most recent file in artifacts/ matching the pattern"""
    files = list(ARTIFACTS_DIR.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No model found {pattern} in {ARTIFACTS_DIR}")
    return max(files, key=lambda p: p.stat().st_mtime)

YOUNG_MODEL = joblib.load(_latest("premium_young_*.joblib"))
REST_MODEL  = joblib.load(_latest("premium_rest_*.joblib"))

# ──────────────────────────────────── helpery
def _norm_risk(med_hist: str) -> float:
    """Returns a 0-1 normalized risk score from one or two diseases (split by ' & ')"""
    total = sum(_RISK.get(d.strip().lower(), 0) for d in med_hist.split("&"))
    return total / 14            # 8+6  (max risk combined)

def _build_dataframe(inp: dict) -> pd.DataFrame:
    """Creates a single-row DataFrame with the training schema"""
    row = {
        "age":                  inp["Age"],
        "number_of_dependants": inp["Number of Dependants"],
        "income_lakhs":         inp["Income in Lakhs"],
        "insurance_plan":       INSURANCE_MAP[inp["Insurance Plan"]],
        "genetical_risk":       inp["Genetical Risk"],
        "gender":               inp["Gender"],
        "region":               inp["Region"],
        "marital_status":       inp["Marital Status"],
        "bmi_category":         inp["BMI Category"],
        "smoking_status":       inp["Smoking Status"],
        "employment_status":    inp["Employment Status"],
        "medical_history":      inp["Medical History"],
    }
    df = pd.DataFrame([row])
    # → Add normalized risk score
    df["normalized_risk_score"] = df["medical_history"].apply(_norm_risk)
    # Drop the column that is not used in the pipeline
    df.drop(columns=["medical_history"], inplace=True)
    return df

# ──────────────────────────────────── main prediction function
def predict(features: dict) -> tuple[float, float]:
    """
    Parameters
    ----------
    features : dict
        The exact dictionary structure passed from the Streamlit form.

    Returns
    -------
    premium      : float
        Predicted health insurance premium in ₹.
    perc_error   : float
        Estimated relative error based on CV MAE.
    """
    df = _build_dataframe(features)

    if features["Age"] <= 25:
        pipe, seg = YOUNG_MODEL, "young"
    else:
        pipe, seg = REST_MODEL, "rest"

    premium = float(pipe.predict(df)[0])
    perc_err_est = _CV_MAE[seg] / premium

    return premium, perc_err_est
