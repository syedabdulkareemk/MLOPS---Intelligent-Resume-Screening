import sys
import os

# Add ml folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ml')))

def run_verification():
    print("Starting verification of TalentLens MLOps project...")
    
    # 1. Test ML matcher
    try:
        from embeddings.encoder import TextEncoder
        from matching.hybrid_matcher import HybridMatcher
        
        encoder = TextEncoder()
        # Mock skill graph for test
        class MockGraph:
            def get_transferable_skills(self, s1, s2): return []
        
        matcher = HybridMatcher(encoder, MockGraph())
        
        resume = {
            "full_text": "Experienced Python developer with 3 years working in AWS and Docker.",
            "skills_list": ["Python", "AWS", "Docker"],
            "years_experience": 3
        }
        
        jd = {
            "full_text": "Looking for a Python engineer with Kubernetes experience. 2 years experience required.",
            "skills_list": ["Python", "Kubernetes", "AWS"],
            "required_experience": 2
        }
        
        scores = matcher.match(resume, jd)
        print("ML Matcher scores:", scores)
        assert scores['final_score'] > 0
        print("ML Matcher verification PASSED.")
    except Exception as e:
        print(f"ML Matcher verification FAILED: {e}")

    # 2. Test FastAPI Endpoints via TestClient
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
        from fastapi.testclient import TestClient
        from main import app
        
        client = TestClient(app)
        resp = client.post("/api/match?candidate_id=1&job_id=2")
        assert resp.status_code == 200
        data = resp.json()
        assert "current_fit" in data
        assert "potential_fit" in data
        print("Backend API verification PASSED.")
    except Exception as e:
        print(f"Backend API verification FAILED: {e}")

if __name__ == "__main__":
    run_verification()
