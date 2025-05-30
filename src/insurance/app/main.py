
import streamlit as st
from insurance.app.prediction_helper import predict, KPI_THRESHOLD

st.set_page_config(page_title="Health-Insurance Premium Estimator",
                   page_icon="💰", layout="centered")

st.title("💰 Health-Insurance Premium Estimator")

with st.form("premium_form", clear_on_submit=False):
    # ——— Row 1
    col1, col2, col3 = st.columns(3)
    age   = col1.number_input("Age", 18, 100, value=30, step=1)
    deps  = col2.number_input("Dependants", 0, 20, value=0, step=1)
    inc   = col3.number_input("Annual income [Lakh ₹]", 0, 200, value=10)

    # ——— Row 2
    col4, col5, col6 = st.columns(3)
    gen_risk = col4.slider("Genetical risk (0-5)", 0, 5, value=0)
    plan     = col5.selectbox("Insurance plan", ["Bronze", "Silver", "Gold"])
    emp_stat = col6.selectbox("Employment status",
                              ["Salaried", "Self-Employed", "Freelancer"])

    # ——— Row 3
    col7, col8, col9 = st.columns(3)
    gender   = col7.selectbox("Gender", ["Male", "Female"])
    marital  = col8.selectbox("Marital status", ["Unmarried", "Married"])
    bmi_cat  = col9.selectbox("BMI category",
                              ["Normal", "Obesity", "Overweight", "Underweight"])

    # ——— Row 4
    col10, col11, col12 = st.columns(3)
    smoke   = col10.selectbox("Smoking status",
                              ["No Smoking", "Regular", "Occasional"])
    region  = col11.selectbox("Region",
                              ["Northwest", "Southeast", "Northeast", "Southwest"])
    med_hist = col12.selectbox("Medical history", [
        "No Disease", "Diabetes", "High blood pressure",
        "Diabetes & High blood pressure", "Thyroid", "Heart disease",
        "High blood pressure & Heart disease", "Diabetes & Thyroid",
        "Diabetes & Heart disease",
    ])

    submitted = st.form_submit_button("Predict")

if submitted:
    feats = {
        "Age": age, "Number of Dependants": deps, "Income in Lakhs": inc,
        "Genetical Risk": gen_risk, "Insurance Plan": plan,
        "Employment Status": emp_stat, "Gender": gender,
        "Marital Status": marital, "BMI Category": bmi_cat,
        "Smoking Status": smoke, "Region": region,
        "Medical History": med_hist,
    }

    try:
        premium, err = predict(feats)
        st.subheader(f"💸 **₹ {premium:,.0f}**")
        st.caption(f"Estimated error: ± {err:.1%}")

        if err <= KPI_THRESHOLD:
            st.success("✅ below 10 % expected error")
        else:
            st.warning("⚠️ error may exceed 10 %")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
