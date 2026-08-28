from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import check_connectivity, lifespan
from app.models.schemas import HealthResponse
from app.routers import careers, graph, skills

app = FastAPI(
    title="SkillGraph AI API",
    description="Career & Skill Relationship Explorer backed by CognoDB",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://skill-graph-git-main-sivasri9833s-projects.vercel.app/", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(careers.router)
app.include_router(skills.router)
app.include_router(graph.router)


@app.get("/api/health", response_model=HealthResponse, tags=["health"])
def health_check():
    db_status = check_connectivity()
    if db_status["status"] == "connected":
        return HealthResponse(status="ok", database="connected")
    return HealthResponse(
        status="degraded",
        database=db_status["status"],
        message=db_status.get("message", "Database unavailable."),
    )
