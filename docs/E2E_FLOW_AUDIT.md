# E2E FLOW AUDIT

Documenting the actual execution chain from Browser to Backend based on runtime verification:

**Upload Resume & Job Description**
↓
**UI Component**: `frontend/src/pages/Screening.tsx` (PASS - Multi-step interactive upload interface implemented).
↓
**API**: `/api/candidates/upload` and `/api/jobs/upload` (PASS - Accepts `multipart/form-data`, creates real memory IDs, dynamically extracts PDF/TXT bytes).
↓
**Parser**: `PyPDF2` + `ml/extraction/parser.py` (PASS - Successfully processes resumes into raw text and distinct semantic bounds).
↓
**Candidate Profile**: (PASS - In-memory structured JSON generation successful).
↓
**Matcher**
↓
**API**: `/api/match` (PASS - Uses real uploaded strings instead of mocks. Evaluates text embeddings on local `all-MiniLM-L6-v2` against target JDs).
↓
**Result**: (PASS - E2E UI rendering of Semantic Fit, Evidence Match, Current Fit, and Transferable Skills directly sourced from python dictionaries is successfully rendered inside `frontend/src/pages/CandidateDetail.tsx`).

## Summary
The **entire primary workflow** has been successfully stripped of all mocked parameters and hardcoded results. The application can receive real `.pdf` and `.txt` files through the browser, run them through local CPU inference, and produce a fully interactive Candidate Twin dashboard containing a working Skill Gap Simulator.
