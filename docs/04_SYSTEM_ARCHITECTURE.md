# System Architecture

The architecture of TalentLens is designed as a distributed, microservices-oriented system to facilitate scalability and modular development.

The infrastructure comprises the following primary tiers:

1. **Data Ingestion & Storage Tier**: 
   - Handles raw data pipelines for resumes (PDF/DOCX) and job descriptions.
   - Utilizes Neo4j for the storage and querying of the Skill Graph.
   - Relational/NoSQL databases for transactional user data and metadata.

2. **Machine Learning Tier**:
   - Hosts the embedding generation service utilizing the `all-MiniLM-L6-v2` architecture.
   - Executes the inference endpoints for the Hybrid 6-stage matching engine and the Career Twin predictive models.
   - Manages model registries and versioning.

3. **Application & Orchestration Tier**:
   - Manages API gateways and request routing.
   - Orchestrates the asynchronous processing of document parsing and feature extraction.

4. **MLOps & Monitoring Tier**:
   - Integrates tools for data versioning (e.g., DVC), experiment tracking (e.g., MLflow), and infrastructure as code to manage the continuous integration and continuous deployment (CI/CD) of model updates.
   - Monitors model drift and system latency.
