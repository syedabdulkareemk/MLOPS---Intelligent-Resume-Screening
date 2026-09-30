# Model Registry and Lifecycle Management

The TalentLens platform utilizes MLflow for robust model registry and lifecycle management, ensuring that all iterations of the parsing and matching models are systematically versioned, tracked, and governed.

## 1. Registry Architecture

We maintain a centralized model registry to decouple the training pipelines from the deployment infrastructure. The registry acts as the single source of truth for all serialized models, metadata, and evaluation metrics.

### Stages of a Model
Every model version progresses through the following formalized lifecycle stages:
- **None/Development:** The model has been trained and logged during an experiment but is not yet validated.
- **Staging:** The model has met baseline validation criteria and is undergoing integration testing (A/B testing, shadow deployment).
- **Production:** The model is actively serving live inference traffic.
- **Archived:** The model is deprecated and retained solely for historical auditing and rollback purposes.

## 2. Promotion Protocol

Model promotion is governed by automated CI/CD checks combined with manual approval gates:
1. **Automated Evaluation:** A newly trained model must outperform the current Production model on a hold-out test set by a predefined margin (e.g., +2% F1-score) to enter Staging.
2. **Shadow Testing:** The Staging model processes live traffic alongside the Production model without affecting user-facing results. The prediction distributions are analyzed for anomalies.
3. **Manual Gate:** Subject matter experts review the model card and fairness metrics before approving the transition from Staging to Production.

## 3. Rollback Mechanism

In the event of severe performance degradation or anomalous predictions detected by our drift monitoring systems, an automated rollback protocol reverts the active endpoint to the immediately preceding Production version within seconds, minimizing downtime and user impact.
