# Viva / Defense Cheat Sheet

- **What is TalentLens?** A recruiter-oriented resume screening platform backed by a reproducible MLOps lifecycle.
- **Why Hybrid Matching?** Keyword matching fails on synonyms; Semantic matching lacks hard evidence. Hybrid uses both.
- **Where does training data come from?** A curated dataset (`candidate_job_pairs_v1.csv`), NOT from recruiter uploads. Total separation of operational vs training data.
- **What is Drift?** When the statistical distribution of real-world resumes diverges from the training dataset.
- **How is deployment handled?** FastAPI loads the model dynamically using the MLflow `@champion` alias.
- **How is reproducible MLOps achieved?** Git tracks code; DVC tracks data; MLflow tracks model artifacts and metrics.
