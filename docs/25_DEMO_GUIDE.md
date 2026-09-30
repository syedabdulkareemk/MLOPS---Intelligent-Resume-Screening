# TalentLens Demo Guide

This guide provides step-by-step instructions for running the TalentLens application locally to demonstrate its parsing and matching capabilities.

## Prerequisites
*   Docker and Docker Compose installed.
*   Minimum 8GB RAM available for container allocation.
*   Git for repository cloning.

## 1. Environment Setup

Clone the repository and navigate to the root directory:
```bash
git clone https://github.com/your-org/TalentLens.git
cd TalentLens
```

Set up the demo environment variables (a sample file is provided):
```bash
cp .env.example .env
```

## 2. Launching the Application

Use Docker Compose to build and start the entire stack (API, PostgreSQL, MongoDB, Redis, MLflow, and the frontend UI):
```bash
docker-compose up --build -d
```
*Note: The initial build may take 10-15 minutes as ML dependencies are downloaded.*

Verify all services are running:
```bash
docker-compose ps
```

## 3. Interacting with the Demo

### 3.1 Accessing the UI
Open your web browser and navigate to: `http://localhost:3000`

### 3.2 Uploading a Job Description
1. Navigate to the **"Jobs"** tab.
2. Click **"Create Job"** and paste a sample software engineering job description.
3. Click **"Save"**. Note the generated Job ID.

### 3.3 Uploading and Parsing a Resume
1. Navigate to the **"Candidates"** tab.
2. Click **"Upload Resume"** and select a PDF file from the `tests/sample_data/resumes/` directory.
3. The system will asynchronously parse the document. Refresh the page after 5 seconds to view the extracted skills and redacted PII.

### 3.4 Executing a Match
1. Navigate to the **"Matching Engine"** tab.
2. Select the uploaded Candidate and the created Job.
3. Click **"Generate Match Score"**.
4. The UI will display the semantic similarity score along with an explainable breakdown of matching and missing skills.

## 4. Teardown
To stop the application and remove the containers, run:
```bash
docker-compose down -v
```
