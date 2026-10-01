# Data Versioning with DVC

We use Data Version Control (DVC) to ensure that every model artifact can be traced back to the exact dataset that produced it.

## DVC Pipeline (`dvc.yaml`)
- `prepare_data`
- `validate_data`
- `preprocess`
- `build_features`
- `train`
- `evaluate`

## Adding New Data
When a new training dataset is created (e.g., `v2_demo.csv`):
1. Replace `candidate_job_pairs_v1.csv`.
2. Run `dvc add data/training/candidate_job_pairs_v1.csv`.
3. Run `git commit -m "Update training data"`.
4. Run `dvc repro` to execute the pipeline and generate the new model.
