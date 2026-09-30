from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Skill(BaseModel):
    name: str
    category: str
    confidence: str
    evidence_count: int
    claimed: bool
    evidence: List[str]

class Candidate(BaseModel):
    candidate_id: str
    name: str
    contact: str
    summary: str
    skills: List[Skill]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]

class JobRequirement(BaseModel):
    skill_name: str
    importance: str
    evidence_expected: str

class JobDescription(BaseModel):
    job_id: str
    title: str
    requirements: List[JobRequirement]
    responsibilities: List[str]
    seniority: str

class MatchResult(BaseModel):
    candidate_id: str
    job_id: str
    current_fit: float
    potential_fit: float
    skill_fit: float
    missing_skills: List[str]
    transferable_skills: List[str]
    matched_skills: List[str]
