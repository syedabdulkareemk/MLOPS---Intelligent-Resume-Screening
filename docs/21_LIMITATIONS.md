# Current Limitations

While TalentLens provides state-of-the-art resume parsing and semantic matching, it is important to acknowledge its current technical and operational constraints.

## 1. Document Parsing Constraints

*   **Complex Formats:** Highly graphical resumes, non-standard layouts (e.g., multi-column designs with embedded charts), and images (scanned PDFs) pose challenges. OCR fallback mechanisms exist but yield lower extraction accuracy.
*   **Language Support:** Currently, the natural language processing pipeline is optimized exclusively for English. Resumes submitted in other languages, or containing mixed languages, may result in degraded parsing and matching performance.

## 2. Semantic Understanding

*   **Contextual Depth:** While semantic matching (via embeddings) is superior to keyword matching, the model may occasionally struggle with nuanced, domain-specific terminology or deeply contextual project descriptions, mistaking them for generic skills.
*   **Soft Skills Extraction:** The accurate extraction and quantification of "soft skills" (e.g., leadership, communication) remain subjective and computationally difficult to verify compared to "hard skills" (e.g., Python, SQL).

## 3. Infrastructure

*   **Cold Start Problem:** New job categories or highly niche roles lacking historical data in our system may initially experience lower quality match recommendations until sufficient data is aggregated.
*   **Real-time Processing:** Synchronous parsing of large documents is computationally expensive; hence, parsing relies on asynchronous queues. Immediate real-time feedback during the upload process is limited.
