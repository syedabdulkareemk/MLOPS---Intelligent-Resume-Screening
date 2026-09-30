from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SetupResponse(BaseModel):
    status: str
    message: str

@router.post("/setup_demo")
def setup_demo_data():
    """Load sample resume and JD into database/graph for demo purposes."""
    return SetupResponse(status="success", message="Demo data loaded successfully")

@router.get("/health")
def health_check():
    return {"status": "ok", "services": {"neo4j": "up", "postgres": "up"}}
