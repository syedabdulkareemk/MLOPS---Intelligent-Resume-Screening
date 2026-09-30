# Model Card: TalentLens Semantic Matcher

## Model Details
*   **Model Name:** TalentLens Semantic Matcher (TL-SM-v1)
*   **Version:** 1.2.0
*   **Architecture:** Dual-Encoder Transformer (based on RoBERTa-base), optimized with cosine similarity head.
*   **Developers:** TalentLens AI Engineering Team
*   **Release Date:** September 2026
*   **License:** Proprietary

## Intended Use
*   **Primary Use Case:** Scoring the semantic similarity and skill overlap between a parsed candidate resume and a target job description.
*   **Out-of-Scope Uses:** Automated hiring or rejection decisions without human oversight; personality profiling; emotional state analysis.

## Training Data
*   **Source:** A proprietary, anonymized dataset of 250,000 historical resume-job pairings, spanning IT, Finance, and Healthcare sectors.
*   **Preprocessing:** All data underwent stringent PII redaction. Features highly correlated with gender, age, and ethnicity were scrubbed.

## Evaluation Data & Metrics
*   **Holdout Set:** 25,000 verified pairs (10% of total data).
*   **Metrics:**
    *   Precision@k (k=5): 0.88
    *   Recall: 0.84
    *   F1-Score: 0.86
    *   Mean Reciprocal Rank (MRR): 0.81

## Ethical Considerations
*   **Bias Mitigation:** Evaluated using Disparate Impact ratios across localized geographic data (as a proxy for demographic groups) ensuring parity within a 5% margin of error.
*   **Transparency:** The model provides explainability outputs via SHAP, highlighting driving features (skills, tenure) for every predicted score.

## Caveats and Recommendations
*   The model heavily weighs explicitly stated technical skills. Candidates using highly abstract language to describe technical work may receive artificially lower scores.
*   It is recommended that human recruiters review the top 20% of generated matches rather than relying solely on the absolute rank of the top 1 candidate.
