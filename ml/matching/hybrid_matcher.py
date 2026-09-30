import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Any

class HybridMatcher:
    """
    6-stage Hybrid Matching Architecture for Resume-Job matching.
    """
    def __init__(self, encoder, skill_graph):
        self.encoder = encoder
        self.skill_graph = skill_graph
        self.tfidf = TfidfVectorizer(stop_words='english')

    def tfidf_match(self, resume_text: str, jd_text: str) -> float:
        """Stage 1: Lexical matching using TF-IDF."""
        if not resume_text or not jd_text:
            return 0.0
        try:
            tfidf_matrix = self.tfidf.fit_transform([resume_text, jd_text])
            return float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        except ValueError:
            return 0.0

    def semantic_match(self, resume_text: str, jd_text: str) -> float:
        """Stage 2: Dense semantic matching."""
        if not resume_text or not jd_text:
            return 0.0
        embeddings = self.encoder.encode([resume_text, jd_text])
        sim = cosine_similarity(embeddings[0:1], embeddings[1:2])[0][0]
        return float(sim)
        
    def canonical_skill_match(self, resume_skills: List[str], jd_skills: List[str]) -> float:
        """Stage 3: Exact canonical skill matching."""
        if not jd_skills: 
            return 0.0
        resume_skills_set = set(s.lower() for s in resume_skills)
        jd_skills_set = set(s.lower() for s in jd_skills)
        overlap = len(resume_skills_set.intersection(jd_skills_set))
        return overlap / len(jd_skills_set)

    def evidence_map_score(self, resume_text: str, jd_skills: List[str]) -> float:
        """Stage 4: Contextual evidence map for skills."""
        if not jd_skills:
            return 0.0
        score = 0
        text_lower = resume_text.lower()
        for skill in jd_skills:
            # Simple contextual check: skill presence in the broader text body
            if skill.lower() in text_lower:
                score += 1
        return score / len(jd_skills)

    def experience_score(self, resume_exp: float, jd_exp_req: float) -> float:
        """Stage 5: Experience heuristic mapping."""
        if jd_exp_req <= 0: 
            return 1.0
        return min(resume_exp / jd_exp_req, 1.0)

    def final_rerank(self, scores: Dict[str, float], weights: Dict[str, float] = None) -> float:
        """Stage 6: Final weighted aggregation."""
        if weights is None:
            weights = {
                'tfidf': 0.15,
                'semantic': 0.25,
                'canonical_skill': 0.25,
                'evidence': 0.15,
                'experience': 0.20
            }
        
        final_score = sum(scores.get(k, 0.0) * weights.get(k, 0.0) for k in weights)
        return final_score

    def match(self, parsed_resume: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, float]:
        """Orchestrates the 6-stage matching process."""
        resume_text = parsed_resume.get('full_text', '')
        jd_text = jd_data.get('full_text', '')
        resume_skills = parsed_resume.get('skills_list', [])
        jd_skills = jd_data.get('skills_list', [])
        resume_exp = parsed_resume.get('years_experience', 0.0)
        jd_exp = jd_data.get('required_experience', 0.0)

        scores = {
            'tfidf': self.tfidf_match(resume_text, jd_text),
            'semantic': self.semantic_match(resume_text, jd_text),
            'canonical_skill': self.canonical_skill_match(resume_skills, jd_skills),
            'evidence': self.evidence_map_score(resume_text, jd_skills),
            'experience': self.experience_score(resume_exp, jd_exp)
        }
        
        scores['final_score'] = self.final_rerank(scores)
        return scores
