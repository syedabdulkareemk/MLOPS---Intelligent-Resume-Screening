import mlflow
import mlflow.sklearn
import numpy as np
import time
import random

def train_mock_model():
    # Set the tracking URI to a local server
    mlflow.set_tracking_uri("http://localhost:5000")
    
    # Set an experiment name
    mlflow.set_experiment("TalentLens_Experiment")
    
    with mlflow.start_run():
        print("Starting mock training loop...")
        
        # Log parameters
        params = {
            "learning_rate": 0.01,
            "n_estimators": 100,
            "max_depth": 5
        }
        mlflow.log_params(params)
        
        # Simulate training loop
        epochs = 10
        loss = 1.0
        accuracy = 0.5
        
        for epoch in range(epochs):
            # Mock metric improvements
            loss -= random.uniform(0.01, 0.05)
            accuracy += random.uniform(0.01, 0.03)
            
            # Log metrics per epoch
            mlflow.log_metric("loss", loss, step=epoch)
            mlflow.log_metric("accuracy", accuracy, step=epoch)
            
            print(f"Epoch {epoch}: loss={loss:.4f}, accuracy={accuracy:.4f}")
            time.sleep(0.5)
            
        # Log a mock model (saving a simple dictionary as a placeholder)
        mock_model = {"model_type": "RandomForest", "status": "trained"}
        # In a real scenario, you'd use mlflow.sklearn.log_model(model, "model")
        
        print("Training complete. Metrics logged to MLflow.")

if __name__ == "__main__":
    train_mock_model()
