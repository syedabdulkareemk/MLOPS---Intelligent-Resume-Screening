# Final Presentation Demo Guide

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
