# Problem Statement – Predictive Health Insurance Premium Model for Shield Insurance

## 1  Background  
Shield Insurance aims to streamline and improve the accuracy of its health-insurance underwriting process. Premiums are currently estimated with a combination of manual rules and actuarial tables, leading to delays and potential pricing inaccuracies. A data-driven, machine-learning approach will allow the company to produce more consistent quotes, reduce underwriting time, and improve customer experience.

## 2  Business Objective  
Create and deploy a predictive model that estimates individual health-insurance premiums using key risk factors:

- **Age**  
- **Smoking status**  
- **Body-Mass Index (BMI)**  
- **Medical history** (e.g., chronic conditions, prior claims)

The model must:

1. **Achieve high accuracy**  
   - ≥ **97 %** overall predictive accuracy.  
   - For at least **95 %** of predictions, the percentage error must be **< 10 %**.

2. **Be universally accessible**  
   - Deployed in the cloud so underwriters can run the model from any location.

3. **Offer an intuitive interface**  
   - Delivered through an interactive **Streamlit** web application.

## 3  Project Scope  

| Phase | Scope | Key Deliverables |
|-------|-------|------------------|
| **Phase 1 — MVP** | • Data ingestion & cleaning<br>• Feature engineering<br>• Model selection & training<br>• Performance evaluation<br>• Streamlit UI<br>• Cloud deployment (e.g., AWS, GCP, or Azure) | • Trained model (> 97 % accuracy)<br>• Deployed REST API / endpoint<br>• Streamlit app for underwriting use |
| **Phase 2 — STP Infrastructure** | • Design straight-through processing (STP) pipeline<br>• Integrate model with policy-issuance systems<br>• Automate quote generation & storage | • Architecture & data-flow diagrams<br>• Cost & effort estimates<br>• Implementation roadmap |

*Only Phase 1 will be executed in this project cycle; Phase 2 will be planned in detail afterward.*

## 4  Success Criteria  

1. **Model Performance**  
   - Validation and test metrics meet or exceed the accuracy thresholds.  
2. **Usability**  
   - Underwriters can generate a quote via the Streamlit app in ≤ 30 seconds.  
3. **Reliability & Availability**  
   - Cloud service uptime ≥ 99.5 %.  
   - Detailed monitoring & alerting in place.  
4. **Security & Compliance**  
   - All data encrypted in transit and at rest.  
   - Compliance with HIPAA / GDPR where applicable.  



