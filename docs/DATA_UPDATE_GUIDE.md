# How Data is Updated

1. **Add new CSV**: Place `new_data.csv` in `data/training/`.
2. **DVC Add**: `dvc add data/training/new_data.csv`
3. **Commit**: `git add data/training/new_data.csv.dvc && git commit -m "New data"`
4. **Reproduce**: `dvc repro`
5. **Evaluate & Register**: The pipeline automatically logs the new model to MLflow.
6. **Promote**: Use the MLflow UI or MLOps Control Center to move the new model to `@champion`.
