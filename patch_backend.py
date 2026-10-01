import re
import os

filepath = "backend/main.py"
with open(filepath, "r") as f:
    content = f.read()

# 1. Update /api/demo to be idempotent and have 5 candidates
demo_endpoint = """@app.post("/api/demo")
def load_demo_workspace():
    DB_JOBS.clear()
    DB_CANDIDATES.clear()
    DB_MATCHES.clear()
    
    job_id = "demo-job-1"
    
    DB_JOBS[job_id] = {
        "id": job_id,
        "title": "Senior MLOps Engineer",
        "full_text": "We are looking for a Senior MLOps Engineer with strong Python and Kubernetes experience. Docker, AWS, and CI/CD pipelines are required. 5 years of experience preferred.",
        "skills_list": ["Python", "Kubernetes", "Docker", "AWS", "CI/CD"],
        "required_experience": 5.0
    }
    
    cands = [
        ("demo-cand-1", "Arun (Strong MLOps)", "Experienced Backend and ML Engineer. Skills: Python, AWS, Docker, Kubernetes, CI/CD.", ["Python", "AWS", "Docker", "Kubernetes", "CI/CD"], 5.0),
        ("demo-cand-2", "Priya (Pure ML)", "Data Scientist focused on AI. Skills: Python, TensorFlow, PyTorch, SQL.", ["Python", "TensorFlow", "PyTorch", "SQL"], 4.0),
        ("demo-cand-3", "Rahul (DevOps)", "Infrastructure engineer. Skills: Docker, AWS, Linux, Terraform, CI/CD.", ["Docker", "AWS", "Linux", "Terraform", "CI/CD"], 6.0),
        ("demo-cand-4", "Karthik (Data Eng)", "Data Engineer. Skills: SQL, Python, Spark, Hadoop.", ["SQL", "Python", "Spark", "Hadoop"], 3.0),
        ("demo-cand-5", "Meena (Junior)", "Recent grad. Skills: Python, HTML, CSS.", ["Python", "HTML", "CSS"], 1.0)
    ]
    
    for cid, name, text, skills, exp in cands:
        DB_CANDIDATES[cid] = {
            "id": cid,
            "name": name,
            "full_text": text,
            "skills_list": skills,
            "years_experience": exp,
            "parsed_sections": {"skills": ", ".join(skills), "full_text": text}
        }
        
    return {"message": "Idempotent demo workspace loaded", "job_id": job_id}
"""

content = re.sub(r'@app\.post\("/api/demo"\).*?(?=@app\.post\("/api/jobs/upload"\))', demo_endpoint, content, flags=re.DOTALL)

# 2. Update /api/match to strictly require MLflow champion model
match_enforcement = """    # STRICT MODEL DEPLOYMENT CHECK
    try:
        import mlflow.pyfunc
        from mlflow import MlflowClient
        client = MlflowClient()
        champion = client.get_model_version_by_alias("TalentLens-Ranker", "champion")
        champion_version = f"v{champion.version}"
        model = mlflow.pyfunc.load_model(f"models:/TalentLens-Ranker@champion")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Matching model not deployed yet. Ask an ML administrator to complete the initial training pipeline.")
        
    import pandas as pd
    feature_df = pd.DataFrame([{
        'semantic_score': scores["semantic"],
        'skill_score': scores["canonical_skill"],
        'evidence_score': scores["evidence"],
        'experience_score': 1.0
    }])
    
    try:
        proba = model.predict_proba(feature_df)[0][1]
        mlflow_prediction = float(proba)
    except:
        mlflow_prediction = float(model.predict(feature_df)[0])
        
    scores["final_score"] = mlflow_prediction
"""

content = re.sub(r'    # MLflow Champion Model Inference.*?scores\["final_score"\] = mlflow_prediction', match_enforcement, content, flags=re.DOTALL)

with open(filepath, "w") as f:
    f.write(content)

print("backend/main.py updated successfully.")
