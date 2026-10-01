# Model Rollback Procedure

If a newly promoted `@champion` model (e.g., V2) begins performing poorly in production, an Admin can execute a Rollback.

## How it works
1. Admin clicks **Rollback to V1** in the MLOps Control Center.
2. The system calls `client.set_registered_model_alias("TalentLens-Ranker", "champion", "1")`.
3. The `@champion` alias immediately points back to Version 1.
4. The FastAPI inference endpoint seamlessly switches back to V1 on the next request.
