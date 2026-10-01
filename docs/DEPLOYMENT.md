# Deployment Strategy

The deployment pattern used in TalentLens relies on **Dynamic Alias Resolution**.

## FastAPI Inference
The backend API (`backend/main.py`) does not store the `.pkl` file locally in its source tree. Instead, it queries the MLflow Tracking Server:
```python
model = mlflow.pyfunc.load_model("models:/TalentLens-Ranker@champion")
```
This means when a model is promoted in MLflow, the backend instantly begins serving the new model without a code deployment.
