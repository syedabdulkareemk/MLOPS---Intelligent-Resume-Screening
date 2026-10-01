# Model Versioning (MLflow)

Models are versioned using MLflow's Model Registry.

- **TalentLens-Ranker**: The single registered model name.
- **Versions**: Automatically incremented by MLflow (V1, V2, etc).
- **Aliases**: We do not hardcode `v1.pkl` into the API. We use MLflow Aliases:
  - `@champion`: The model currently serving live traffic.
  - `@challenger`: A newly trained model waiting for evaluation.

When the MLOps pipeline runs, it registers the artifact to MLflow and assigns the appropriate alias.
