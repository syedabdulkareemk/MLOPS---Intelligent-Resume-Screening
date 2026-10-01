# System Architecture

TalentLens is divided into two distinct but interconnected systems: the **Operational Application (Inference)** and the **MLOps Pipeline (Training)**.

## Operational Application (Recruiter Flow)
1. **Recruiter** uploads Resumes and Job Descriptions.
2. **Parser** extracts skills and text (using PyPDF2 and custom NER).
3. **Hybrid Matcher** calculates Semantic (SentenceTransformers), Lexical (TF-IDF), and Evidence scores.
4. **FastAPI Backend** loads the `@champion` model from MLflow.
5. **Prediction** - The model ranks the candidate.
6. **Frontend** renders the Candidate Career Twin and Skill Gaps.

## MLOps Pipeline (Admin Flow)
1. **Training Data** (`candidate_job_pairs_v1.csv`) is versioned via DVC.
2. **DVC Repro** runs the data preparation, feature engineering, and model training (Scikit-Learn).
3. **MLflow** tracks metrics (F1, Precision) and registers the model artifacts.
4. **Model Registry** promotes models (e.g., to `@champion` or `@challenger`).
5. **Drift Detection** compares reference data to incoming inference data.
6. **Retraining** triggers if drift is detected, creating V2.
