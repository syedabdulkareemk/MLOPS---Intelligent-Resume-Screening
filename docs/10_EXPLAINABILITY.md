# Explainability

To foster trust and facilitate human-in-the-loop oversight, TalentLens incorporates a dedicated Explainability framework.

The system is mandated to provide transparent rationales for all generated rankings and recommendations. This is achieved by decomposing the aggregated scores from the Hybrid 6-stage engine.

For any given match, the system surfaces the contributing factors:
- **Semantic Evidence**: Highlighting the specific text spans in the resume that most closely aligned with the `all-MiniLM-L6-v2` embeddings of the job requirements.
- **Graph Evidence**: Visualizing the localized Neo4j sub-graph that connects the candidate's existing skills to the required skills via identified adjacencies.
This deterministic mapping ensures that recruiters and hiring managers can validate the algorithmic logic, mitigating the "black box" phenomenon prevalent in standard AI matching systems.
