from fastapi import APIRouter, Depends, HTTPException
from neo4j import Session
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.database import get_session
from app.models.schemas import SkillDetail, SkillSummary
from app.queries import GET_SKILL_DETAILS, LIST_SKILLS

router = APIRouter(prefix="/api/skills", tags=["skills"])


def _node_to_skill(node) -> SkillSummary:
    return SkillSummary(
        name=node["name"],
        category=node.get("category", ""),
        description=node.get("description", ""),
        difficulty=node.get("difficulty", ""),
    )


@router.get("", response_model=list[SkillSummary])
def list_skills(session: Session = Depends(get_session)):
    try:
        result = session.run(LIST_SKILLS)
        return [
            SkillSummary(
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
        raise HTTPException(status_code=500, detail="Failed to retrieve skills.")


@router.get("/{skill_name}", response_model=SkillDetail)
def get_skill(skill_name: str, session: Session = Depends(get_session)):
    try:
        result = session.run(GET_SKILL_DETAILS, skill_name=skill_name)
        record = result.single()
        if not record or record["s"] is None:
            raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found.")

        skill = record["s"]
        return SkillDetail(
            name=skill["name"],
            category=skill.get("category", ""),
            description=skill.get("description", ""),
            difficulty=skill.get("difficulty", ""),
            prerequisites=[_node_to_skill(n) for n in record["prerequisites"] if n],
            leads_to=[_node_to_skill(n) for n in record["leads_to"] if n],
            related=[_node_to_skill(n) for n in record["related"] if n],
        )
    except HTTPException:
        raise
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Failed to retrieve skill details.")
