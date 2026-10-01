# How Code is Updated

1. **Branch**: `git checkout -b feature/new-ranker`
2. **Modify Code**: Edit `ml/monitoring/pipeline.py`.
3. **Test**: Run `pytest`.
4. **Commit & Push**: `git commit -m "Update algorithm"`
5. **CI/CD**: GitHub Actions runs the tests.
6. **DVC Repro**: If ML behavior changed, run `dvc repro` to generate a new model artifact.
7. **MLflow**: Register the new model version.
