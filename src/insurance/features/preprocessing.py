"""
Builds a reusable ColumnTransformer / Pipeline with
- MinMax scaling for numerical cols
- One-Hot encoding for categoricals
"""
from __future__ import annotations
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

NUM_COLS = [
    "age",
    "number_of_dependants",
    "income_lakhs",
    "insurance_plan",          # label-encoded (1-3)
    "normalized_risk_score",
]

CAT_COLS = [
    "gender",
    "region",
    "marital_status",
    "bmi_category",
    "smoking_status",
    "employment_status",
    # "income_level" deleted due to too high VIF
]

def make_preprocessor() -> ColumnTransformer:
    """
    Returns a ColumnTransformer that:
    • scales NUM_COLS with MinMax  
    • one-hot-encodes CAT_COLS (drop_first=True)
    """
    return ColumnTransformer(
        [
            ("num", MinMaxScaler(), NUM_COLS),
            ("cat", OneHotEncoder(drop="first", dtype=int), CAT_COLS),
        ],
        remainder="drop",
    )

def make_preprocessor_young() -> ColumnTransformer:
    """
    Variant of make_preprocessor() that includes 'genetical_risk' as a numerical feature.
    """
    num_cols = [
        "age",
        "number_of_dependants",
        "income_lakhs",
        "insurance_plan",
        "normalized_risk_score",
        "genetical_risk"
    ]

    cat_cols = [
        "gender",
        "region",
        "marital_status",
        "bmi_category",
        "smoking_status",
        "employment_status"
    ]

    return ColumnTransformer(
        [
            ("num", MinMaxScaler(), num_cols),
            ("cat", OneHotEncoder(drop="first", dtype=int), cat_cols),
        ],
        remainder="drop",
    )
