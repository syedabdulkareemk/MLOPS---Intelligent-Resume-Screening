# FEATURE AUDIT

| Feature | Code Exists | UI Exists | Backend Connected | Dependency | Runtime Tested | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Resume parsing | Yes (`parser.py`) | Yes (`Screening.tsx`) | Yes | `pypdf2` | Yes | PASS |
| JD parsing | Yes | Yes | Yes | `pypdf2` | Yes | PASS |
| SentenceTransformer embeddings | Yes (`encoder.py`) | N/A | Yes | CPU | Yes | PASS |
| 6-stage Hybrid Matching | Yes (`hybrid_matcher.py`) | N/A | Yes | CPU | Yes | PASS |
| Candidate Career Twin | Yes (Models) | Yes (`CandidateDetail.tsx`) | Yes | None | Yes | PASS |
| Evidence-backed skills | Yes (Models) | Yes | Yes | None | Yes | PASS |
| Current Fit | Yes (`main.py`) | Yes | Yes | None | Yes | PASS |
| Potential Fit | Yes (`main.py`) | Yes | Yes | Neo4j | Yes (Mock fallback) | PASS |
| Transferable Skills | Yes (`main.py`) | Yes | Yes | Neo4j | Yes (Mock fallback) | PASS |
| Skill Gap Simulator | Yes | Yes | Yes | None | Yes | PASS |
| Neo4j Skill Graph | Yes (`skill_graph.py`) | Yes (Graceful UI fallback)| Yes | Neo4j | No | NOT VERIFIED |
| Candidate ↔ Job Graph | No | Yes (Graceful UI fallback)| No | Neo4j | No | NOT IMPLEMENTED |
| Career Path | Yes (`skill_graph.py`) | No | No | Neo4j | No | PARTIAL |
| Explainable matching | Yes | Yes | Yes | None | Yes | PASS |
| PostgreSQL | Yes | N/A | No (Using Memory DB) | PostgreSQL | No | NOT VERIFIED |
| MLflow | Yes (`pipeline.py`)| Yes (MLOps UI)| Yes | Local SQLite | Yes | PASS |
| DVC | Yes (`dvc.yaml`) | N/A | N/A | DVC | No | NOT VERIFIED |
| Drift Monitoring | Yes (`pipeline.py`) | Yes (MLOps UI)| Yes | MLflow | Yes | PASS |
| CI/CD | Yes (`.github`) | N/A | N/A | GitHub | No | NOT VERIFIED |
| UI Dashboard | Yes (`App.tsx`) | Yes | Yes | None | Yes | PASS |
| UI Screening Page | Yes (`Screening.tsx`) | Yes | Yes | None | Yes | PASS |
