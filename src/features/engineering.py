import pandas as pd

def clean_age(val):
    """Cleans age values by removing the first digit if the number has more than two digits."""
    val_str = str(val)
    if len(val_str) > 2:
        return int(val_str[1:])
    return val

def get_salary_bounds(col):
    """Calculates IQR-based bounds for income outlier removal."""
    Q1, Q3 = col.quantile([0.25, 0.90])
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and preprocesses the input DataFrame:
    - Handles missing values
    - Removes duplicates
    - Fixes data entry errors
    - Handles outliers
    - Standardizes categorical values
    """
    df = df.copy()

    # Standardize column names
    df.columns = df.columns.str.replace(" ", "_").str.lower()

    # Drop missing and duplicate rows
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Clean number_of_dependants (negative -> absolute)
    if "number_of_dependants" in df.columns:
        df["number_of_dependants"] = df["number_of_dependants"].abs()

    # Clean age values and filter by minimum legal age
    if "age" in df.columns:
        df["age"] = df["age"].apply(clean_age)
        df = df[df["age"] >= 18].copy()


    # Handle income outliers
    if "income_lakhs" in df.columns:
        min_income, max_income = get_salary_bounds(df["income_lakhs"])
        df = df[df["income_lakhs"] < max_income].copy()


    # Standardize smoking_status categories
    if "smoking_status" in df.columns:
        df = df.assign(
        smoking_status = df["smoking_status"].replace({
            'Smoking=0': "No Smoking",
            'Does Not Smoke': "No Smoking",
            'Not Smoking': "No Smoking"
        })
)
    return df