# Machine Learning Pipeline

The machine learning pipeline within TalentLens is formalized to ensure reproducibility and robustness.

1. **Data Preprocessing**: Unstructured text from resumes and job descriptions undergoes tokenization, lemmatization, and stop-word removal. Entity extraction algorithms identify skills, experiences, and educational background.
2. **Feature Engineering**: 
   - **Vector Generation**: Textual features are encoded into dense numerical vectors using `all-MiniLM-L6-v2`.
   - **Graph Features**: Node centrality and path distances are extracted from the Neo4j Skill Graph.
3. **Model Training & Fine-tuning**: While the core embeddings utilize pre-trained models, domain-specific fine-tuning is applied to adapt the semantic representations to specialized industry terminology.
4. **Inference**: During inference, candidate profiles are projected into the vector space and evaluated against job requirements using cosine similarity, complemented by graph-based scoring.
5. **Evaluation**: Pipeline performance is continuously evaluated against historical placement data, utilizing metrics such as Mean Reciprocal Rank (MRR) and Normalized Discounted Cumulative Gain (NDCG).
