# Hybrid 6-Stage Matching Engine

The core evaluation mechanism of TalentLens is the Hybrid 6-Stage Matching Engine, designed to synthesize multiple evaluation paradigms.

1. **Hard Constraint Filtering**: Initial deterministic filtering based on non-negotiable criteria (e.g., work authorization, location, baseline education).
2. **Semantic Similarity Scoring**: Computation of cosine similarity between the `all-MiniLM-L6-v2` embeddings of the candidate's profile and the job description to establish baseline semantic fit.
3. **Skill Graph Alignment**: Querying the Neo4j database to evaluate the structural overlap of the candidate's skill set with the required skills, accounting for direct matches and adjacent/prerequisite skills.
4. **Experience Weighting**: Algorithmic adjustment of scores based on the temporal depth and relevance of professional experience.
5. **Anomaly & Verification Checks**: Identification of inconsistencies or improbable timelines within the candidate profile.
6. **Aggregated Scoring & Ranking**: Final synthesis of scores from stages 2-4, utilizing a weighted ensemble approach to produce a definitive candidate ranking.
