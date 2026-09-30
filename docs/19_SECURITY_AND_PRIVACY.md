# Security and Privacy

Protecting candidate data is a foundational requirement for TalentLens. This document outlines the security architecture and privacy-preserving mechanisms implemented across the platform.

## 1. Data Security

### 1.1 Encryption
*   **In Transit:** All communications between clients, APIs, and microservices are encrypted using TLS 1.3.
*   **At Rest:** Data stored in PostgreSQL, MongoDB, and S3 buckets is encrypted at rest using AES-256 via AWS KMS.

### 1.2 Access Control
*   **Role-Based Access Control (RBAC):** API access is strictly governed by RBAC. Employers can only access anonymized candidate profiles and their own job postings.
*   **Infrastructure Security:** Our Kubernetes clusters run within a private VPC. Ingress is restricted via API gateways and Web Application Firewalls (WAF).

## 2. Privacy and PII Handling

Resumes inherently contain highly sensitive Personally Identifiable Information (PII).

### 2.1 Automated Redaction
During the initial parsing phase, before data is persisted to long-term storage or used for model inference, we employ a PII detection and redaction pipeline (leveraging Microsoft Presidio and custom SpaCy NER models).
*   **Redacted Entities:** Names, phone numbers, email addresses, physical addresses, and links to personal profiles are stripped and replaced with generic tokens (e.g., `[NAME_REDACTED]`).

### 2.2 Compliance
*   **GDPR and CCPA:** TalentLens is designed with compliance in mind. We provide automated mechanisms for user data deletion requests ("Right to be Forgotten") and data export ("Right to Portability").
*   **Data Retention:** Raw resume files are permanently deleted after 30 days unless explicit extended consent is provided by the candidate.

## 3. Vulnerability Management
*   Regular automated dependency scanning is integrated into our CI/CD pipelines.
*   Annual third-party penetration testing is conducted on our production infrastructure and web application interfaces.
