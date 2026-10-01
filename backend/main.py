from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import os
import sys
import uuid
import PyPDF2
from io import BytesIO

# Add ml folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ml')))

from models import Candidate, JobDescription, MatchResult
import routers

# Import actual ML components
try:
    from embeddings.encoder import TextEncoder
    from matching.hybrid_matcher import HybridMatcher
    from graph.skill_graph import SkillGraphDB
    from extraction.parser import ResumeParser
    
    encoder = TextEncoder()
    # If Neo4j is unavailable, we still instantiate it. We'll handle connection errors internally.
    skill_graph = SkillGraphDB("bolt://localhost:7687", "neo4j", "password")
    matcher = HybridMatcher(encoder, skill_graph)
    resume_parser = ResumeParser()
    ML_ENGINE_AVAILABLE = True
except Exception as e:
    print(f"ML Engine initialization failed: {e}")
    ML_ENGINE_AVAILABLE = False
    matcher = None
    resume_parser = None

app = FastAPI(title="TalentLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router, prefix="/api")

# IN-MEMORY DATABASE (Docker-less persistence for runtime demo)
DB_JOBS = {}
DB_CANDIDATES = {}
DB_MATCHES = {}

def extract_text(file: UploadFile) -> str:
    content = file.file.read()
    if file.filename.lower().endswith('.pdf'):
        try:
            reader = PyPDF2.PdfReader(BytesIO(content))
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e:
            print(f"PDF extraction failed: {e}")
            return content.decode('utf-8', errors='ignore')
    return content.decode('utf-8', errors='ignore')

@app.get("/")
def read_root():
    return {"message": "Welcome to TalentLens MLOps API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/system/health")
def system_health():
    return {
        "api": "healthy",
        "postgresql": "unavailable",
        "neo4j": "unavailable",
        "mlflow": "unavailable",
        "ml_engine": "healthy" if ML_ENGINE_AVAILABLE else "unavailable"
    }

@app.post("/api/demo")
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
@app.post("/api/jobs/upload")
def upload_job(title: str = Form(...), file: UploadFile = File(...)):
    text = extract_text(file)
    job_id = str(uuid.uuid4())
    
    # Very basic naive skill extraction for JD since JD parser isn't heavily implemented
    potential_skills = ["Python", "Kubernetes", "Docker", "AWS", "CI/CD", "Machine Learning", "FastAPI", "React", "TypeScript", "SQL"]
    extracted = [s for s in potential_skills if s.lower() in text.lower()]
    
    DB_JOBS[job_id] = {
        "id": job_id,
        "title": title,
        "full_text": text,
        "skills_list": extracted if extracted else ["Python"],
        "required_experience": 3.0 # Default heuristic
    }
    return {"job_id": job_id, "title": title}

@app.post("/api/candidates/upload")
def upload_resume(file: UploadFile = File(...)):
    text = extract_text(file)
    cand_id = str(uuid.uuid4())
    
    if ML_ENGINE_AVAILABLE and resume_parser:
        parsed = resume_parser.parse(text)
    else:
        parsed = {"skills": "", "full_text": text}
        
    potential_skills = ["Python", "Kubernetes", "Docker", "AWS", "CI/CD", "Machine Learning", "FastAPI", "React", "TypeScript", "SQL", "Terraform"]
    extracted = [s for s in potential_skills if s.lower() in text.lower()]
    
    DB_CANDIDATES[cand_id] = {
        "id": cand_id,
        "name": file.filename.split('.')[0].replace('_', ' '),
        "full_text": text,
        "skills_list": extracted,
        "years_experience": 3.0, # Default heuristic
        "parsed_sections": parsed
    }
    return {"candidate_id": cand_id, "name": DB_CANDIDATES[cand_id]["name"]}

@app.get("/api/jobs")
def get_jobs():
    return list(DB_JOBS.values())

@app.get("/api/candidates")
def get_candidates():
    return list(DB_CANDIDATES.values())

@app.get("/api/candidates/{cand_id}")
def get_candidate(cand_id: str):
    if cand_id not in DB_CANDIDATES:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return DB_CANDIDATES[cand_id]

@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    if job_id not in DB_JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    return DB_JOBS[job_id]

@app.post("/api/match")
def run_match(candidate_id: str, job_id: str, simulate_skill: str = None):
    if not ML_ENGINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="ML engine is unavailable")
        
    if candidate_id not in DB_CANDIDATES or job_id not in DB_JOBS:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")
        
    resume = dict(DB_CANDIDATES[candidate_id]) # Copy
    jd = dict(DB_JOBS[job_id])
    
    if simulate_skill:
        # Avoid modifying the actual DB record permanently for simulation
        sim_skills = list(resume.get("skills_list", []))
        sim_skills.append(simulate_skill)
        resume["skills_list"] = sim_skills
        resume["full_text"] += f" Also familiar with {simulate_skill}."
    
    scores = matcher.match(resume, jd)
    
    # STRICT MODEL DEPLOYMENT CHECK
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

    
    # Graph Transferable Skills fallback since Neo4j is offline
    transferable = []
    missing = [skill for skill in jd["skills_list"] if skill not in resume["skills_list"]]

    
    # Mock some graph relationships for the demo
    graph_edges = {
        "Docker": "Kubernetes",
        "Python": "FastAPI",
        "JavaScript": "React"
    }
    for r_skill in resume["skills_list"]:
        if r_skill in graph_edges and graph_edges[r_skill] in missing:
            transferable.append(f"{graph_edges[r_skill]} (from {r_skill})")
            
    potential_fit = scores["final_score"]
    if transferable:
        potential_fit = min(1.0, scores["final_score"] + (0.15 * len(transferable)))
        
    match_result = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "current_fit": scores["final_score"],
        "potential_fit": potential_fit,
        "skill_fit": scores["canonical_skill"],
        "semantic_fit": scores["semantic"],
        "evidence_fit": scores["evidence"],
        "missing_skills": missing,
        "transferable_skills": transferable,
        "matched_skills": list(set(resume["skills_list"]).intersection(jd["skills_list"])),
        "scores_breakdown": scores,
        "model_version_used": champion_version
    }
    
    # Save match
    DB_MATCHES[f"{candidate_id}_{job_id}"] = match_result
    
    return match_result

@app.get("/api/matches/{candidate_id}/{job_id}")
def get_match(candidate_id: str, job_id: str):
    match_key = f"{candidate_id}_{job_id}"
    if match_key not in DB_MATCHES:
        raise HTTPException(status_code=404, detail="Match not found")
    return DB_MATCHES[match_key]

# --- MLOps Endpoints ---

@app.post("/api/mlops/pipeline")
def run_mlops_pipeline():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
        from ml.monitoring.pipeline import run_training_pipeline
        result = run_training_pipeline(dataset_path="../data/training/candidate_job_pairs_v1.csv", version="v1")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mlops/drift")
def run_drift_check():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
        from ml.monitoring.pipeline import check_drift
        result = check_drift(reference_path="../data/monitoring/reference_jobs.csv", current_path="../data/monitoring/current_jobs_drift_demo.csv")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mlops/retrain")
def run_mlops_retrain():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
        from ml.monitoring.pipeline import run_training_pipeline
        result = run_training_pipeline(dataset_path="../data/training/candidate_job_pairs_v2_demo.csv", version="v2")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mlops/promote")
def run_mlops_promote():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
        from ml.monitoring.pipeline import promote_model
        return promote_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mlops/rollback")
def run_mlops_rollback():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
        from ml.monitoring.pipeline import rollback_model
        return rollback_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mlops/status")
def get_mlops_status():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
        from ml.monitoring.pipeline import get_deployment_status
        return get_deployment_status()
    except Exception as e:
        return {"champion_version": None, "challenger_version": None}

