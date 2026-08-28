from fastapi import APIRouter, Depends, HTTPException, Query
from neo4j import Session
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.database import get_session
from app.models.schemas import (
    CareerDetail,
    CareerSummary,
    LearningPathItem,
    LearningPathResponse,
    ProjectSummary,
    SearchResult,
    SkillSummary,
    StatsResponse,
)
from app.queries import (
    GET_CAREER_DETAILS,
    GET_LEARNING_PATH_FULL,
    GET_STATS,
    LIST_CAREERS,
    SEARCH_NODES,
)

router = APIRouter(prefix="/api/careers", tags=["careers"])


def _node_to_skill(node) -> SkillSummary | None:
    if node is None:
        return None
    return SkillSummary(
        name=node["name"],
        category=node.get("category", ""),
        description=node.get("description", ""),
        difficulty=node.get("difficulty", ""),
    )


def _node_to_project(node) -> ProjectSummary | None:
    if node is None:
        return None
    return ProjectSummary(
        name=node["name"],
        description=node.get("description", ""),
        difficulty=node.get("difficulty", ""),
    )


@router.get("", response_model=list[CareerSummary])
def list_careers(session: Session = Depends(get_session)):
    try:
        result = session.run(LIST_CAREERS)
        return [
            CareerSummary(
                name=record["name"],
                description=record["description"],
                category=record["category"],
                difficulty=record["difficulty"],
            )
            for record in result
        ]
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Failed to retrieve careers.")


@router.get("/stats/summary", response_model=StatsResponse)
def get_stats(session: Session = Depends(get_session)):
    try:
        result = session.run(GET_STATS)
        record = result.single()
        if not record:
            return StatsResponse(careers=0, skills=0, relationships=0)
        return StatsResponse(
            careers=record["careers"],
            skills=record["skills"],
            relationships=record["relationships"],
        )
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics.")


@router.get("/search", response_model=list[SearchResult])
def search_careers_and_skills(
    q: str = Query(..., min_length=1, description="Search query"),
    session: Session = Depends(get_session),
):
    try:
        result = session.run(SEARCH_NODES, query=q)
        return [
            SearchResult(
                name=record["name"],
                type=record["type"],
                description=record["description"] or "",
            )
            for record in result
        ]
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Search failed.")


@router.get("/{career_name}", response_model=CareerDetail)
def get_career(career_name: str, session: Session = Depends(get_session)):
    try:
        result = session.run(GET_CAREER_DETAILS, career_name=career_name)
        record = result.single()
        if not record or record["c"] is None:
            raise HTTPException(status_code=404, detail=f"Career '{career_name}' not found.")

        career = record["c"]
        skills = [_node_to_skill(s) for s in record["skills"] if s is not None]
        projects = [_node_to_project(p) for p in record["projects"] if p is not None]

        return CareerDetail(
            name=career["name"],
            description=career["description"],
            category=career["category"],
            difficulty=career["difficulty"],
            skills=[s for s in skills if s],
            projects=[p for p in projects if p],
        )
    except HTTPException:
        raise
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Failed to retrieve career details.")


@router.get("/{career_name}/learning-path", response_model=LearningPathResponse)
def get_learning_path(career_name: str, session: Session = Depends(get_session)):
    """
    Generate an ordered learning path by traversing PREREQUISITE_OF
    relationships across multiple hops for all skills required by the career.
    """
    try:
        # Verify career exists
        check = session.run(GET_CAREER_DETAILS, career_name=career_name)
        check_record = check.single()
        if not check_record or check_record["c"] is None:
            raise HTTPException(status_code=404, detail=f"Career '{career_name}' not found.")

        result = session.run(GET_LEARNING_PATH_FULL, career_name=career_name)
        path_items: list[LearningPathItem] = []
        seen: set[str] = set()

        for idx, record in enumerate(result, start=1):
            name = record["name"]
            if name in seen:
                continue
            seen.add(name)
            path_items.append(
                LearningPathItem(
                    order=len(path_items) + 1,
                    name=name,
                    category=record["category"] or "",
                    description=record["description"] or "",
                    difficulty=record["difficulty"] or "",
                )
            )

        return LearningPathResponse(career=career_name, path=path_items)
    except HTTPException:
        raise
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Failed to generate learning path.")
