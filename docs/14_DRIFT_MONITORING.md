# Drift Monitoring and Observability

To maintain high fidelity in our matching algorithms over time, TalentLens implements continuous drift monitoring using Evidently AI. This ensures that the platform adapts to evolving job market trends and shifting resume formatting standards.

## 1. Types of Drift Monitored

### 1.1 Data Drift (Covariate Shift)
We monitor the statistical distribution of incoming feature vectors (e.g., extracted skills, experience duration, education levels) against the reference distribution of the training data.
- **Metric:** Population Stability Index (PSI), Wasserstein Distance for continuous variables.
- **Threshold:** A PSI > 0.2 triggers an automated alert indicating significant feature drift.

### 1.2 Concept Drift
Concept drift occurs when the relationship between the features and the target variable changes (e.g., a specific skill previously considered highly relevant for a role is no longer demanded).
- **Metric:** We track the decay of proxy metrics such as user acceptance rate of recommended matches.

## 2. Monitoring Pipeline

1. **Log Collection:** Inference requests and responses, along with delayed user feedback, are asynchronously logged to a data lake.
2. **Batch Analysis:** A scheduled nightly job computes drift metrics over a rolling 7-day window.
3. **Alerting:** If thresholds are breached, alerts are routed to the MLOps engineering team via PagerDuty and Slack.
4. **Triggered Retraining:** Sustained data drift automatically triggers a data curation pipeline and subsequent model retraining workflow, ensuring the system self-heals over time.
