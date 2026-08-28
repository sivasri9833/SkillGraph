from fastapi import APIRouter, Depends, HTTPException, Query
from neo4j import Session
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.database import get_session
from app.models.schemas import ConnectionResponse, ConnectionStep, GraphData, GraphEdge, GraphNode
from app.queries import FIND_SKILL_CONNECTION, GET_CAREER_GRAPH

router = APIRouter(prefix="/api/graph", tags=["graph"])


def _slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")


@router.get("/career/{career_name}", response_model=GraphData)
def get_career_graph(career_name: str, session: Session = Depends(get_session)):
    """Return nodes and edges for React Flow visualization of a career's skill graph."""
    try:
        result = session.run(GET_CAREER_GRAPH, career_name=career_name)
        record = result.single()
        if not record or record["c"] is None:
            raise HTTPException(status_code=404, detail=f"Career '{career_name}' not found.")

        career = record["c"]
        nodes: dict[str, GraphNode] = {}
        edges: list[GraphEdge] = []

        career_id = f"career-{_slugify(career['name'])}"
        nodes[career_id] = GraphNode(
            id=career_id,
            label=career["name"],
            type="career",
            description=career.get("description", ""),
            difficulty=career.get("difficulty", ""),
            category=career.get("category", ""),
        )

        for skill in record["skills"]:
            if skill is None:
                continue
            skill_id = f"skill-{_slugify(skill['name'])}"
            nodes[skill_id] = GraphNode(
                id=skill_id,
                label=skill["name"],
                type="skill",
                description=skill.get("description", ""),
                difficulty=skill.get("difficulty", ""),
                category=skill.get("category", ""),
            )
            edges.append(
                GraphEdge(
                    id=f"{career_id}-{skill_id}",
                    source=career_id,
                    target=skill_id,
                    label="REQUIRES",
                )
            )

        edge_set: set[str] = set()
        for rel in record["skill_relationships"]:
            if rel is None or rel.get("source") is None:
                continue
            source_id = f"skill-{_slugify(rel['source'])}"
            if not rel.get("source") or not rel.get("target"):
                continue
            target_id = f"skill-{_slugify(rel['target'])}"
            if source_id not in nodes:
                continue
            if target_id not in nodes:
                continue
            edge_key = f"{source_id}-{target_id}-{rel['type']}"
            if edge_key in edge_set:
                continue
            edge_set.add(edge_key)
            edges.append(
                GraphEdge(
                    id=edge_key,
                    source=source_id,
                    target=target_id,
                    label=rel["type"],
                )
            )

        return GraphData(nodes=list(nodes.values()), edges=edges)
    except HTTPException:
        raise
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Failed to retrieve career graph.")


@router.get("/connections", response_model=ConnectionResponse)
def find_connections(
    source: str = Query(..., description="Source skill name"),
    target: str = Query(..., description="Target skill name"),
    session: Session = Depends(get_session),
):
    """
    Find the shortest path between two skills using multi-hop graph traversal.
    Demonstrates a query that is natural in a graph DB but awkward with recursive SQL joins.
    """
    try:
        result = session.run(FIND_SKILL_CONNECTION, source_name=source, target_name=target)
        record = result.single()

        if not record or record["path"] is None:
            return ConnectionResponse(
                source=source,
                target=target,
                found=False,
                message=f"No connection found between '{source}' and '{target}' within 6 hops.",
            )

        path = record["path"]
        path_nodes = [node["name"] for node in path.nodes]
        steps: list[ConnectionStep] = []

        for rel in path.relationships:
            steps.append(
                ConnectionStep(
                    from_node=rel.start_node["name"],
                    to_node=rel.end_node["name"],
                    relationship=rel.type,
                    from_type=list(rel.start_node.labels)[0] if rel.start_node.labels else "Unknown",
                    to_type=list(rel.end_node.labels)[0] if rel.end_node.labels else "Unknown",
                )
            )

        return ConnectionResponse(
            source=source,
            target=target,
            found=True,
            hops=len(steps),
            path_nodes=path_nodes,
            steps=steps,
            message=f"Found a {len(steps)}-hop path from '{source}' to '{target}'.",
        )
    except ServiceUnavailable:
        raise HTTPException(status_code=503, detail="Database is currently unavailable.")
    except Neo4jError:
        raise HTTPException(status_code=500, detail="Failed to find skill connections.")
