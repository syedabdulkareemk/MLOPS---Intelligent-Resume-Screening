# API Documentation

The TalentLens core matching engine is exposed via a robust, RESTful FastAPI interface. The API is designed for low-latency synchronous operations (e.g., health checks) and asynchronous task delegation for heavy computational workloads (e.g., resume parsing).

## 1. Authentication
All endpoints (excluding `/health`) require a JWT Bearer token passed in the `Authorization` header.

## 2. Endpoints

### 2.1 Health Check
**Endpoint:** `GET /health`
**Description:** Validates system uptime and database connectivity.
**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.2.0",
  "database": "connected",
  "model_registry": "reachable"
}
```

### 2.2 Resume Upload and Parsing
**Endpoint:** `POST /api/v1/resume/parse`
**Content-Type:** `multipart/form-data`
**Description:** Accepts a PDF/DOCX file, queues it for processing via Celery, and returns a task tracking ID.
**Response (202 Accepted):**
```json
{
  "task_id": "c8a9f0e1-...",
  "status": "processing_queued"
}
```

### 2.3 Job Matching
**Endpoint:** `POST /api/v1/match`
**Content-Type:** `application/json`
**Description:** Compares a parsed candidate profile against a target job description and returns a semantic match score and feature importance breakdown.
**Request Payload:**
```json
{
  "candidate_id": "uuid-...",
  "job_id": "uuid-..."
}
```
**Response (200 OK):**
```json
{
  "match_score": 0.87,
  "confidence": 0.92,
  "key_overlapping_skills": ["Python", "Kubernetes", "Machine Learning"],
  "missing_critical_skills": ["Go"]
}
```

## 3. Rate Limiting and Error Handling
The API enforces a rate limit of 100 requests per minute per user to prevent abuse. Standard HTTP status codes (400, 401, 403, 404, 422, 500) are utilized, with structured JSON error payloads detailing the nature of the failure.
