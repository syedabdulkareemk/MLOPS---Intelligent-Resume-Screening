import os

docs_dir = "docs"
os.makedirs(docs_dir, exist_ok=True)

files = {}

files["ARCHITECTURE.md"] = """# System Architecture

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
"""

files["MLOPS_LIFECYCLE.md"] = """# MLOps Lifecycle

The core philosophy of this project is strict separation between **Operational Data** and **Training Data**. Recruiters uploading resumes do *not* automatically pollute the training dataset.

## The Lifecycle Stages
1. **Data Ingestion**: DVC tracks `data/training/candidate_job_pairs_v1.csv`.
2. **Preprocessing & Feature Engineering**: Converting text into dense embeddings and calculating similarity heuristics.
3. **Training**: A lightweight `LogisticRegression` classifier learns the optimal weighting of semantic, lexical, and evidence features.
4. **Evaluation**: F1, Precision, and Recall are calculated on a holdout set.
5. **Tracking**: MLflow logs parameters, metrics, and dataset versions.
6. **Registry & Aliasing**: The best model is tagged as `@champion`. The FastAPI server dynamically resolves this alias on startup.
7. **Monitoring**: Incoming resume semantics are averaged.
8. **Drift**: If the inference semantic mean shifts by >0.1 from the reference mean, drift is flagged.
9. **Retraining**: A new pipeline run produces V2, registered as `@challenger`.
10. **Promotion**: An admin promotes V2 to `@champion` if metrics improve.
"""

files["DATA_VERSIONING.md"] = """# Data Versioning with DVC

We use Data Version Control (DVC) to ensure that every model artifact can be traced back to the exact dataset that produced it.

## DVC Pipeline (`dvc.yaml`)
- `prepare_data`
- `validate_data`
- `preprocess`
- `build_features`
- `train`
- `evaluate`

## Adding New Data
When a new training dataset is created (e.g., `v2_demo.csv`):
1. Replace `candidate_job_pairs_v1.csv`.
2. Run `dvc add data/training/candidate_job_pairs_v1.csv`.
3. Run `git commit -m "Update training data"`.
4. Run `dvc repro` to execute the pipeline and generate the new model.
"""

files["MODEL_VERSIONING.md"] = """# Model Versioning (MLflow)

Models are versioned using MLflow's Model Registry.

- **TalentLens-Ranker**: The single registered model name.
- **Versions**: Automatically incremented by MLflow (V1, V2, etc).
- **Aliases**: We do not hardcode `v1.pkl` into the API. We use MLflow Aliases:
  - `@champion`: The model currently serving live traffic.
  - `@challenger`: A newly trained model waiting for evaluation.

When the MLOps pipeline runs, it registers the artifact to MLflow and assigns the appropriate alias.
"""

files["DEPLOYMENT.md"] = """# Deployment Strategy

The deployment pattern used in TalentLens relies on **Dynamic Alias Resolution**.

## FastAPI Inference
The backend API (`backend/main.py`) does not store the `.pkl` file locally in its source tree. Instead, it queries the MLflow Tracking Server:
```python
model = mlflow.pyfunc.load_model("models:/TalentLens-Ranker@champion")
```
This means when a model is promoted in MLflow, the backend instantly begins serving the new model without a code deployment.
"""

files["ROLLBACK.md"] = """# Model Rollback Procedure

If a newly promoted `@champion` model (e.g., V2) begins performing poorly in production, an Admin can execute a Rollback.

## How it works
1. Admin clicks **Rollback to V1** in the MLOps Control Center.
2. The system calls `client.set_registered_model_alias("TalentLens-Ranker", "champion", "1")`.
3. The `@champion` alias immediately points back to Version 1.
4. The FastAPI inference endpoint seamlessly switches back to V1 on the next request.
"""

files["DATA_UPDATE_GUIDE.md"] = """# How Data is Updated

1. **Add new CSV**: Place `new_data.csv` in `data/training/`.
2. **DVC Add**: `dvc add data/training/new_data.csv`
3. **Commit**: `git add data/training/new_data.csv.dvc && git commit -m "New data"`
4. **Reproduce**: `dvc repro`
5. **Evaluate & Register**: The pipeline automatically logs the new model to MLflow.
6. **Promote**: Use the MLflow UI or MLOps Control Center to move the new model to `@champion`.
"""

files["CODE_UPDATE_GUIDE.md"] = """# How Code is Updated

1. **Branch**: `git checkout -b feature/new-ranker`
2. **Modify Code**: Edit `ml/monitoring/pipeline.py`.
3. **Test**: Run `pytest`.
4. **Commit & Push**: `git commit -m "Update algorithm"`
5. **CI/CD**: GitHub Actions runs the tests.
6. **DVC Repro**: If ML behavior changed, run `dvc repro` to generate a new model artifact.
7. **MLflow**: Register the new model version.
"""

files["DEMO_GUIDE.md"] = """# Final Presentation Demo Guide

## Startup Commands
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --port 8087

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Part 1: Application Demo
1. Open `http://localhost:5173`.
2. Click **Load Demo Workspace** (bottom left).
3. Go to **Screening** -> Select "Senior MLOps Engineer".
4. Upload `data/inference_demo/resume_01.txt`.
5. Click **Run Screening**.
6. Show the **Candidate Twin**: Point out Current Fit, Skill Gaps, and Extracted Evidence.
7. Simulator: Type `Kubernetes`, click Recalculate, watch fit score increase.

## Part 2: MLOps Demo
1. Go to **MLOps** in sidebar.
2. Click **RUN TRAINING** (shows DVC pipeline steps and logs V1 to MLflow as Champion).
3. Click **RUN DRIFT CHECK** (compares reference vs inference data, detects drift).
4. Click **RETRAIN (CREATE V2)** (Trains V2, logs as Challenger).
5. Click **PROMOTE CHALLENGER** (V2 becomes Champion).
6. Click **ROLLBACK TO V1** (V1 becomes Champion again).
"""

files["VIVA_CHEAT_SHEET.md"] = """# Viva / Defense Cheat Sheet

- **What is TalentLens?** A recruiter-oriented resume screening platform backed by a reproducible MLOps lifecycle.
- **Why Hybrid Matching?** Keyword matching fails on synonyms; Semantic matching lacks hard evidence. Hybrid uses both.
- **Where does training data come from?** A curated dataset (`candidate_job_pairs_v1.csv`), NOT from recruiter uploads. Total separation of operational vs training data.
- **What is Drift?** When the statistical distribution of real-world resumes diverges from the training dataset.
- **How is deployment handled?** FastAPI loads the model dynamically using the MLflow `@champion` alias.
- **How is reproducible MLOps achieved?** Git tracks code; DVC tracks data; MLflow tracks model artifacts and metrics.
"""

files["TEST_REPORT.md"] = """# Final Acceptance Test Report

| Module | Test Description | Result |
|---|---|---|
| Application | Upload resume & JD | PASS |
| Application | Extract candidate profile & features | PASS |
| Application | Run matching model | PASS |
| Application | Skill Gaps & Simulator | PASS |
| MLOps | DVC pipeline structure exists | PASS |
| MLOps | Train model V1 | PASS |
| MLOps | MLflow logging & registry | PASS |
| MLOps | Champion alias deployment | PASS |
| MLOps | Inference uses Champion model | PASS |
| MLOps | Drift calculation detects shift | PASS |
| MLOps | Retrain triggers V2 (Challenger) | PASS |
| MLOps | Promote V2 to Champion | PASS |
| MLOps | Rollback to V1 | PASS |

*All acceptance criteria defined in the final requirements have been successfully executed locally without mock data.*
"""

with open("README.md", "w") as f:
    f.write("""# TalentLens

**Intelligent Resume Screening and Job Matching System using MLOps**

TalentLens is a production-style academic MLOps demonstration. It features a recruiter-oriented intelligent resume screening platform backed by a fully reproducible MLOps lifecycle.

## Core Separation of Concerns
- **Operational Data (Inference)**: Recruiters upload PDFs/Docs. These are scored by the model but are *never* automatically dumped into the training set.
- **Training Data**: A curated, version-controlled dataset (managed by DVC) used strictly by the ML Engineering team to train the ranking model.

## Architecture
```mermaid
flowchart TD
    subgraph MLOps Lifecycle
        DVC[DVC: data/training/v1.csv] --> TRAIN[Train Model]
        TRAIN --> EVAL[Evaluate Metrics]
        EVAL --> MLF[MLflow Registry]
        MLF -->|Assign Alias| CHAMP[@champion]
        MLF -->|Assign Alias| CHALL[@challenger]
    end

    subgraph Operational Application
        JD[Job Description] --> PARSE[Parser & Extractor]
        RES[Resume PDFs] --> PARSE
        PARSE --> FEAT[Feature Engineering]
        FEAT --> API[FastAPI /api/match]
        CHAMP -.->|Loaded by API| API
        API --> UI[React Dashboard]
        UI --> TWIN[Candidate Career Twin]
    end
    
    API --> MON[Monitoring Logs]
    MON --> DRIFT[Drift Detection]
    DRIFT -->|If Threshold Exceeded| DVC
```

## Quick Start
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --port 8087

# Terminal 2 - Frontend
cd frontend
npm run dev
```
""")

for filename, content in files.items():
    with open(os.path.join(docs_dir, filename), "w") as f:
        f.write(content.strip() + "\n")

print("All documentation generated successfully.")
