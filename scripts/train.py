import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ml.monitoring.pipeline import run_training_pipeline
print("Training model...")
res = run_training_pipeline(dataset_path="data/training/features_v1.csv", version="v1")
print(f"Trained model: {res}")
