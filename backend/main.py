from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from models import Candidate, JobDescription, MatchResult
import routers

app = FastAPI(title="TalentLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router, prefix="/api")

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
        "ml_engine": "healthy"
    }

@app.post("/api/jobs/upload")
def upload_job(file: UploadFile = File(...)):
    # Mock parsing
    return {"job_id": "job_123", "title": "Mock Job"}

@app.post("/api/candidates/upload")
def upload_resume(file: UploadFile = File(...)):
    # Mock extraction
    return {"candidate_id": "cand_123", "name": "Mock Candidate"}

@app.post("/api/match")
def run_match(candidate_id: str, job_id: str):
    # Mock match result
    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "current_fit": 0.85,
        "potential_fit": 0.92,
        "skill_fit": 0.80,
        "missing_skills": ["Kubernetes"],
        "transferable_skills": ["Docker", "AWS"],
        "matched_skills": ["Python", "FastAPI"]
    }
