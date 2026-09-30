# Module Design

The TalentLens system is modularized into distinct, cohesive components:

1. **Document Processing Engine**: Responsible for Optical Character Recognition (OCR) and Natural Language Processing (NLP) based extraction of entities from unstructured text.
2. **Embedding Service**: A dedicated microservice exposing endpoints for vectorizing textual data using the `all-MiniLM-L6-v2` transformer model.
3. **Graph Operations Module**: Interfaces directly with the Neo4j database to perform CRUD operations on the Skill Graph and execute Cypher queries for pathfinding and adjacency analysis.
4. **Matching Engine Core**: Implements the Hybrid 6-stage pipeline, orchestrating sequential filters and scoring mechanisms to evaluate candidate-job fit.
5. **Career Twin Simulator**: Analyzes temporal skill acquisition data to forecast career progressions and generate personalized learning pathways.
6. **Explainability Service**: Generates human-readable rationales for system recommendations by tracing matching scores back to specific semantic alignments and graph relationships.
