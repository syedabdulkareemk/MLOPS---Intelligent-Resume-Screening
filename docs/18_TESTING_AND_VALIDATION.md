# Testing and Validation Framework

Quality assurance in TalentLens encompasses both traditional software testing and specialized machine learning model validation to ensure system reliability and predictive accuracy.

## 1. Software Testing

Our testing pyramid prioritizes fast, deterministic unit tests, supported by comprehensive integration and end-to-end tests.

*   **Unit Tests:** Built with `pytest`. We mock external dependencies (e.g., database connections, cloud storage) to validate internal business logic, parsing algorithms, and API routing.
*   **Integration Tests:** Ensure that the API, database, and Redis message broker communicate correctly. These are run in isolated Docker containers during the CI phase.
*   **Load Testing:** Conducted using `Locust` to simulate concurrent API requests, ensuring the inference endpoints can maintain P99 latency requirements under peak loads.

## 2. ML Model Validation

Before any model is registered for Staging, it must pass a suite of offline validation checks:

*   **Performance Benchmarking:** The model must achieve a baseline precision, recall, and F1-score on a golden holdout dataset of historically verified job-candidate matches.
*   **Slice-based Testing:** Global metrics can obscure localized failures. We evaluate model performance across different job categories (e.g., Engineering vs. Sales) and demographic proxies to ensure equitable performance.
*   **Perturbation Testing (Invariance):** The model should produce consistent scores even if minor formatting changes or synonyms are introduced into the resume.
*   **Directional Expectation Testing:** Adding a relevant skill to a candidate's profile should never decrease their match score for a corresponding job.

## 3. Shadow Testing in Production
Once deployed to Staging, the model shadows live traffic. We compute the difference in predictions between the Staging and Production models. If the divergence exceeds expected bounds without corresponding improvements in offline metrics, the promotion is halted.
