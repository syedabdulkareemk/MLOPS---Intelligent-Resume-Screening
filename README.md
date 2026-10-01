# TalentLens

**Intelligent Resume Screening and Job Matching System using MLOps**

TalentLens is a complete, production-style academic demonstration of an MLOps lifecycle integrated with a functional HR application. 

## What is TalentLens?
TalentLens is an AI-powered recruitment platform designed to batch-process and rank candidate resumes against specific job descriptions. It uses a 6-stage Hybrid Matching Engine (Lexical, Semantic, Skill, Evidence, Experience) to extract features, and a trainable ML model to output a final probabilistic fit score.

## Who Uses It?
1. **Recruiters / HR**: Use the front-end application to create jobs, batch-upload resumes, view ranked lists, and inspect Candidate Career Twins.
2. **ML Administrators / ML Engineers**: Use the built-in MLOps Control Center to track datasets, train models, detect drift, and promote/rollback models using MLflow.

## Data Separation (Crucial Architecture)
* **Training Data**: Resides in `data/training/` and is strictly versioned by DVC. It consists of `candidate_job_pairs.csv` with known semantic/skill/evidence features and labels.
* **Inference Data**: Resume PDFs and TXT files uploaded by recruiters in real-time. This data is scored by the model but **never** automatically added to the training set.

## MLOps Lifecycle Explained

### How is V1 Trained & Deployed?
1. The ML Admin runs the initial training pipeline from the MLOps Control Center.
2. The pipeline executes: `DVC Data Validation -> Preprocessing -> Feature Building -> Training -> Evaluation`.
3. The trained model is logged to **MLflow**.
4. The model is registered as `TalentLens-Ranker` and assigned the `@champion` alias.
5. The FastAPI backend dynamically serves whichever model currently holds the `@champion` alias.

### How does recruiter screening work?
1. A recruiter selects a Job.
2. They drag-and-drop multiple resumes.
3. The backend parses each resume, extracts skills and features, and queries the `@champion` model.
4. The frontend renders a ranked table, offering deep-dives into "Current Fit", "Potential Fit", and Skill Gaps.

### How is monitoring performed and drift handled?
Every inference request is logged. Periodically, the ML Admin clicks **Run Drift Check**, which mathematically compares the incoming feature distribution (`current_jobs.csv`) against the baseline (`reference_jobs.csv`). 

### Retraining, Promotion & Rollback
* **Retraining**: If drift is detected, the Admin prepares new data and clicks **Retrain**. This trains V2 and logs it to MLflow as the `@challenger`.
* **Promotion**: The Admin compares V1 and V2 metrics. Clicking **Promote Challenger** swaps the `@champion` alias to V2. Inference immediately switches to V2.
* **Rollback**: If V2 underperforms, clicking **Rollback to V1** swaps the alias back, instantly restoring V1 to production.

## Maintenance Guide

### How do I update training data?
Add a new CSV to `data/training/`. Run `dvc add data/training/your_file.csv` and `git commit`. Run the training pipeline to produce a new model version.

### How do I update ML code?
Modify `ml/monitoring/pipeline.py`. Commit your changes using Git. The new Git SHA will be automatically picked up and logged in the MLOps Control Center during the next training run.

### How do I reproduce the model?
Run `dvc repro`. This guarantees that the specific Git commit, DVC data version, and MLflow run are identically recreated.

## Quick Start
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --port 8087

# Terminal 2 - Frontend
cd frontend
npm run dev
```

*Navigate to `http://localhost:5173/mlops` first to train V1, then use the Recruiter Workspace!*
