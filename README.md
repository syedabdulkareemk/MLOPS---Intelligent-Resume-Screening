# TalentLens

**Intelligent Resume Screening and Job Matching System using MLOps**

TalentLens is a complete MLOps-driven intelligent recruitment platform featuring multi-facet hybrid semantic matching, candidate career twins, and job-market drift detection.

## 1. Project Identity
**Project Title**: Intelligent Resume Screening and Job Matching System using MLOps
**Product**: TalentLens

## 2. One Paragraph Explanation
TalentLens moves beyond simplistic keyword ATS filters by parsing resumes and job descriptions into structured data, embedding them with dense semantic models, and executing a sophisticated 6-stage hybrid matching pipeline. It creates a "Candidate Career Twin" that tracks both claimed skills and evidence-backed competencies, utilizing a Neo4j skill graph to reason about transferable skills and project career pathways, all orchestrated through a rigorous MLOps lifecycle tracking drift and model versioning.

## 3. Core Problem
Traditional Applicant Tracking Systems (ATS) rely on exact keyword matching, punishing candidates for using synonymous terms and completely failing to recognize transferable skills. They treat a resume as a single block of text rather than a structured evidence portfolio, resulting in poor candidate fit approximations.

## 4. Solution
TalentLens parses inputs into explicit requirements and candidate experiences, semantically evaluates their alignment, and utilizes a knowledge graph to bridge skill gaps (e.g., scoring a candidate with Docker experience highly for a Kubernetes role).

## 5. Core Features
- **Resume Parsing & JD Parsing**: Deterministic extraction of skills, education, and experience.
- **Skill Normalization**: Canonical resolution of terms (e.g., JS -> JavaScript).
- **Hybrid Matching Engine**: 6-stage fallback pipeline.
- **Candidate Career Twin**: Evidence-backed vs. claimed skill tracking.
- **Current vs. Potential Fit**: Transferable skill scoring.
- **Skill Gap Simulator**: Interactive GUI to test skill acquisitions.
- **Neo4j Skill Graph**: Candidate-job bipartite relationships and career paths.
- **Explainability**: Traces scores directly back to resume bullet points.
- **MLOps**: MLflow model registry, DVC data versioning, drift monitoring, and CI/CD.

## 6. Architecture
*(See `docs/04_SYSTEM_ARCHITECTURE.md` for full Mermaid diagrams)*
The system utilizes a React/Vite frontend querying a FastAPI Python backend. Data is persisted in PostgreSQL (structured application data) and Neo4j (graph relationships). The ML Engine runs locally using CPU-friendly Transformer embeddings.

## 7. Technology Stack
- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: FastAPI, Python
- **NLP / Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`), scikit-learn
- **Database / Graph**: PostgreSQL, Neo4j
- **MLOps**: MLflow, DVC, GitHub Actions, Docker Compose

## 8. Repository Structure
- `/frontend`: React + Vite dashboard
- `/backend`: FastAPI endpoints and Pydantic schemas
- `/ml`: Core NLP, Embeddings, Matching Engine, Graph logic, and Monitoring
- `/docs`: Academic documentation suite, handoff instructions, and test reports
- `/pipelines` & `/tests`: Verification and data ingestion logic

## 9. How Matching Works (Hybrid Engine)
1. **Lexical Retrieval**: TF-IDF / BM25 for rapid keyword checks.
2. **Semantic Retrieval**: Dense vector similarities for contextual alignment.
3. **Structured Skill Matching**: Exact and fuzzy canonical matches.
4. **Evidence Matching**: Mapping JD requirements to explicit resume bullet evidence.
5. **Experience Compatibility**: Normalizing seniority/years of experience.
6. **Final Reranking**: Weighted fusion of the above 5 stages into a final score.

## 10. Candidate Career Twin
Instead of representing a candidate as a list `[Python, Docker]`, TalentLens stores a State Object mapping claimed competencies to the exact resume section that provides evidence of its application, ensuring transparent confidence intervals.

## 11. Skill Graph
Neo4j maps relations like `[Docker] -PREREQUISITE_OF-> [Kubernetes]`. Candidates are connected to Jobs via dynamically generated `SUPPORTS` or `MISSING` edges.

## 12. Current Fit vs Potential Fit
- **Current Fit**: The aggregate hybrid score based strictly on current evidence.
- **Potential Fit**: The hypothetical score calculated by identifying transferable skills traversing the Neo4j graph and simulating their acquisition.

## 13. Skill Gap Simulator
A UI tool that allows recruiters to inject a missing skill into the candidate's twin and mathematically re-run the 6-stage matcher to observe the updated score dynamically.

## 14. MLOps Lifecycle
`Data Ingestion -> Preprocessing -> Feature Extraction -> Training -> Evaluation -> MLflow Registry -> Deployment -> Drift Detection -> Retraining`.

## 15. Docker Environment
The production infrastructure requires Docker Compose to orchestrate PostgreSQL, Neo4j, and MLflow simultaneously.

## 16. LOCAL DEVELOPMENT WITHOUT DOCKER
The following can run natively without Docker:
- Frontend (`npm run dev`)
- FastAPI Backend (`uvicorn`)
- CPU ML Engine (`all-MiniLM-L6-v2`)
- Unit and Integration Tests

Requires Docker: PostgreSQL, Neo4j, MLflow.

## 17. FULL DOCKER STARTUP
```bash
git clone <repo>
cd TalentLens
docker-compose up -d

# Backend
cd backend
python -m uvicorn main:app --port 8000

# Frontend
cd frontend
npm run dev
```

## 18. Verification Checklist
- [x] Frontend / Backend API connection
- [x] CPU ML Engine Matcher Execution
- [x] Load Testing (50 requests, <2.5s P95 latency)
- [ ] PostgreSQL Persistence (Requires Docker)
- [ ] Neo4j Graph Traversal (Requires Docker)
- [ ] MLflow Logging (Requires Docker)

## 19. Known Limitations
- CPU inference for semantic embeddings limits batch screening concurrency.
- Potential Fit relies heavily on a robust, pre-seeded Skill Taxonomy graph.
- Market Drift requires chronological snapshots to operate meaningfully.

## 20. Future Scope
- Transition to Vector Databases (e.g., Milvus/Pinecone) for O(1) semantic lookups.
- Federated learning models for cross-organizational resume parsing without exposing PII.

## 21. AI ASSISTANT HANDOFF
Please refer to `docs/AI_HANDOFF.md` before making any further architectural modifications.
