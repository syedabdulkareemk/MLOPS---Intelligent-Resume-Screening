# Data Card: TalentLens Historical Hiring Dataset

## Dataset Overview
*   **Dataset Name:** TalentLens Historical Hiring Dataset (TL-HHD)
*   **Version:** 2026.01
*   **Total Instances:** 250,000 resume-job description pairs.
*   **Total Size:** ~1.2 GB (compressed, JSON format)

## Collection Process
*   **Origin:** Data aggregated from partner enterprise ATS (Applicant Tracking Systems) between 2020 and 2025 under strict data sharing agreements.
*   **Labeling:** Positive matches (1) indicate instances where a candidate was invited to at least a second-round interview. Negative matches (0) indicate early rejection or non-progression.
*   **Consent:** All data usage complies with original candidate terms of service at the time of application.

## Dataset Composition
*   **Sectors:** Technology (45%), Finance (30%), Healthcare (15%), Administration/Other (10%).
*   **Class Balance:** 30% Positive matches, 70% Negative matches (down-sampled from original highly skewed distribution).

## Preprocessing and Privacy (PII)
*   **Redaction pipeline:** Applied Microsoft Presidio to remove names, emails, phone numbers, exact addresses, and institutional identifiers.
*   **Normalization:** Job titles standardized against the O*NET occupational database. Date ranges converted into normalized duration integers (e.g., "Months of Experience").

## Known Limitations and Bias
*   **Temporal Bias:** The dataset leans heavily on hiring practices during the 2020-2023 tech boom. It may not accurately reflect recent market contractions or emerging niche roles (e.g., highly specific Generative AI engineering roles).
*   **Survivorship Bias:** The definition of a "positive match" relies on historical human recruiter decisions, inherently encoding any latent human biases present in the partner organizations during the collection period.

## Access and Maintenance
*   **Access Control:** Strictly limited to internal TalentLens ML engineering staff. Not available for public download.
*   **Update Frequency:** Annually audited and refreshed with recent operational data to mitigate concept drift.
