# MLOps Lifecycle

The core philosophy of this project is strict separation between **Operational Data** and **Training Data**. Recruiters uploading resumes do *not* automatically pollute the training dataset.

## The Lifecycle Stages
1. **Data Ingestion**: DVC tracks `data/training/candidate_job_pairs_v1.csv`.
2. **Preprocessing & Feature Engineering**: Converting text into dense embeddings and calculating similarity heuristics.
3. **Training**: A lightweight `LogisticRegression` classifier learns the optimal weighting of semantic, lexical, and evidence features.
4. **Evaluation**: F1, Precision, and Recall are calculated on a holdout set.
5. **Tracking**: MLflow logs parameters, metrics, and dataset versions.
6. **Registry & Aliasing**: The best model is tagged as `@champion`. The FastAPI server dynamically resolves this alias on startup.
7. **Monitoring**: Incoming resume semantics are averaged.
8. **Drift**: If the inference semantic mean shifts by >0.1 from the reference mean, drift is flagged.
9. **Retraining**: A new pipeline run produces V2, registered as `@challenger`.
10. **Promotion**: An admin promotes V2 to `@champion` if metrics improve.
