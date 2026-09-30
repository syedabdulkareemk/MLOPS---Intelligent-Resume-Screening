# Reference Repositories

TalentLens builds upon and is inspired by several foundational open-source projects in the domains of HR tech, natural language processing, and semantic search. We acknowledge the contributions of the following reference repositories:

## 1. Milan
*   **Description:** An advanced NLP pipeline for enterprise resume parsing and entity extraction. Milan provides the foundational heuristics used in our early OCR and section-segmentation logic.
*   **License:** MIT License
*   **Attribution:** Milan Contributors

## 2. MatchLens
*   **Description:** A semantic similarity matching framework optimized for short-text documents and job descriptions. We utilized their comparative benchmarks to validate our own bi-encoder architecture.
*   **License:** Apache License 2.0
*   **Attribution:** MatchLens Research Group

## 3. SkillGraph Navigator
*   **Description:** An open-source ontological mapping of technology skills and industry competencies. TalentLens utilizes subsets of this graph to augment our skill embeddings and resolve synonyms.
*   **License:** GNU General Public License v3.0 (GPLv3) / MIT Dual License
*   **Attribution:** SkillGraph Open Source Community

## 4. AI Resume Matcher
*   **Description:** A baseline implementation of TF-IDF and keyword-overlap techniques for matching resumes to job descriptions. This repository served as our initial baseline model against which our deep learning models were evaluated.
*   **License:** MIT License
*   **Attribution:** AI Resume Matcher Project
