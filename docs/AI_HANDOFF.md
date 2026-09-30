# AI ASSISTANT HANDOFF

## PROJECT STATUS
Core architecture implemented.
Frontend and FastAPI can run without Docker.
Full infrastructure integration requires Docker.

## CURRENTLY WORKING
- Frontend (React + Vite + Tailwind)
- FastAPI Backend (API routes established)
- Deterministic ML Engine (`sentence-transformers`, `all-MiniLM-L6-v2`)
- Hybrid Matcher (6-stage deterministic pipeline)
- Python integration tests (`tests/verify.py` and `tests/load_test.py`)

## INFRASTRUCTURE REQUIRED (Unverified without Docker)
- PostgreSQL
- Neo4j
- MLflow tracking server
- DVC remote backend operations

## KNOWN ISSUES / LIMITATIONS
- CPU inference is slower than GPU inference (batch processing may bottleneck).
- Potential fit is a graph/model estimate, not a guaranteed hiring prediction.
- Graph quality depends entirely on the initial skill taxonomy seeded into Neo4j.
- Production-scale load has not been tested beyond 50 concurrent requests.
- Full Docker verification could not be executed on the current machine because Docker is unavailable.

## DO NOT CHANGE
- Do not delete the Neo4j graph integration (`ml/graph/skill_graph.py`).
- Do not replace MLflow integrations with fake API responses (use actual MLflow logging).
- Do not hardcode semantic scores in the hybrid matcher.
- Do not remove MLOps components (drift detection, DVC, etc.).
- Do not add random technologies or rewrite the architecture.

## NEXT STEPS
For the next agent or human developer initializing this project on a Docker-capable machine:
1. Copy `.env.example` to `.env` and set secure passwords.
2. Run `docker-compose up -d`
3. Verify service health using `docker ps`
4. Run backend (`python -m uvicorn main:app --port 8000`)
5. Run frontend (`npm run dev`)
6. Execute browser E2E (upload real JD and Resume)
7. Run MLOps pipeline (`python mlflow_tracker.py`)
8. Generate final test report

## IMPORTANT FILES
- `backend/main.py`: Entrypoint for FastAPI.
- `ml/matching/hybrid_matcher.py`: Core logic for Candidate/Job matching.
- `ml/embeddings/encoder.py`: Manages the local `SentenceTransformers` model.
- `ml/graph/skill_graph.py`: Neo4j graph querying and structure.
- `docker-compose.yml`: Infrastructure topology.
- `dvc.yaml`: Data versioning pipeline.
- `.github/workflows/ci.yml`: CI/CD pipeline definition.
