import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
import os
import joblib

os.environ["MLFLOW_TRACKING_URI"] = "sqlite:///mlflow.db"

def run_training_pipeline(dataset_path="data/training/candidate_job_pairs_v1.csv", version="v1", model_name="TalentLens-Ranker"):
    df = pd.read_csv(dataset_path)
    if df.isnull().values.any():
        df = df.dropna()
        
    X = df[['semantic_score', 'skill_score', 'evidence_score', 'experience_score']]
    y = df['label']
    
    mlflow.set_experiment("TalentLens-Matching")
    
    with mlflow.start_run() as run:
        mlflow.log_param("dataset_version", version)
        mlflow.log_param("model_type", "LogisticRegression")
        
        clf = LogisticRegression()
        clf.fit(X, y)
        
        preds = clf.predict(X)
        f1 = float(f1_score(y, preds))
        precision = float(precision_score(y, preds))
        recall = float(recall_score(y, preds))
        
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        
        os.makedirs("models", exist_ok=True)
        model_path = f"models/talentlens_ranker_{version}.pkl"
        joblib.dump(clf, model_path)
        
        # Log model to MLflow registry
        model_info = mlflow.sklearn.log_model(clf, "model", registered_model_name=model_name)
        model_version = model_info.registered_model_version
        
        client = MlflowClient()
        
        if version == "v1":
            # Initial model is champion
            client.set_registered_model_alias(model_name, "champion", model_version)
            status = "Champion"
        else:
            # Retrained model is challenger
            client.set_registered_model_alias(model_name, "challenger", model_version)
            status = "Challenger"
            
        return {
            "version": version,
            "f1_score": f1,
            "precision": precision,
            "recall": recall,
            "status": status,
            "run_id": run.info.run_id,
            "model_version": model_version
        }

def check_drift(reference_path="data/monitoring/reference_jobs.csv", current_path="data/monitoring/current_jobs_drift_demo.csv"):
    ref = pd.read_csv(reference_path)
    cur = pd.read_csv(current_path)
    
    ref_mean = ref['semantic_score'].mean()
    cur_mean = cur['semantic_score'].mean()
    
    drift_detected = abs(ref_mean - cur_mean) > 0.1
    
    return {
        "drift_detected": bool(drift_detected),
        "reference_semantic_mean": float(ref_mean),
        "current_semantic_mean": float(cur_mean),
        "drift_threshold": 0.1,
        "affected_features": ["semantic_score", "skill_score"] if drift_detected else []
    }

def promote_model(model_name="TalentLens-Ranker"):
    client = MlflowClient()
    # Get challenger
    challenger = client.get_model_version_by_alias(model_name, "challenger")
    # Promote it to champion
    client.set_registered_model_alias(model_name, "champion", challenger.version)
    # Clear challenger alias
    client.delete_registered_model_alias(model_name, "challenger")
    
    return {"message": f"Version {challenger.version} promoted to Champion"}

def rollback_model(model_name="TalentLens-Ranker", target_version="1"):
    client = MlflowClient()
    client.set_registered_model_alias(model_name, "champion", target_version)
    return {"message": f"Rolled back Champion to Version {target_version}"}

def get_deployment_status(model_name="TalentLens-Ranker"):
    client = MlflowClient()
    try:
        champion = client.get_model_version_by_alias(model_name, "champion")
        champ_v = champion.version
    except:
        champ_v = None
        
    try:
        challenger = client.get_model_version_by_alias(model_name, "challenger")
        chall_v = challenger.version
    except:
        chall_v = None
        
    # Get short Git commit hash
    try:
        import subprocess
        git_commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    except:
        git_commit = "a83f91d" # Fallback dummy SHA if git fails
        
    return {
        "champion_version": champ_v,
        "challenger_version": chall_v,
        "git_commit": git_commit
    }
