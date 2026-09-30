# MLOps Architecture for TalentLens

This document outlines the Machine Learning Operations (MLOps) lifecycle implemented for the TalentLens project. Our goal is to ensure reproducible, trackable, and reliable model deployments.

## 1. Pipeline Orchestration (DVC)

We use Data Version Control (DVC) to manage our ML pipelines and version our large datasets and model artifacts.

The pipeline is defined in `dvc.yaml` and consists of the following stages:
- **Data Ingestion**: Pulls raw data via the *Milan* integration.
- **Preprocessing**: Cleans data and extracts features using *AI Resume Matcher*.
- **Training**: Trains the core matching models for *MatchLens*.
- **Evaluation**: Assesses model performance against holdout sets.

Run the pipeline using: `dvc repro`

## 2. Experiment Tracking (MLflow)

All experiments, hyperparameter tuning, and model artifacts are tracked using MLflow.
- **Script**: `mlflow_tracker.py` demonstrates a mock training loop logging metrics (loss, accuracy).
- **Server**: Configured to log to a local tracking server (`http://localhost:5000`).

To start the UI:
```bash
mlflow ui -p 5000
```

## 3. Model Monitoring (Drift Detection)

Monitoring model performance in production is critical, especially in a dynamic environment like the job market.
- **Script**: `ml/monitoring/drift.py`
- **Purpose**: Detects job-market drift by comparing the distribution of current Job Descriptions against a reference dataset (historical JDs). If the divergence exceeds a threshold, an alert is triggered, signaling the need for model retraining.

## 4. Continuous Integration / Continuous Deployment (CI/CD)

We use GitHub Actions to automate testing and linting.
- **Workflow File**: `.github/workflows/ci.yml`
- **Checks**: 
  - `flake8` for code quality and style compliance.
  - `pytest` for unit and integration testing.
- **Triggers**: On every push and pull request to the `main` or `master` branches.
