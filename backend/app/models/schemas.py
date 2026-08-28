from pydantic import BaseModel, Field


class CareerSummary(BaseModel):
    name: str
    description: str
    category: str
    difficulty: str


class SkillSummary(BaseModel):
    name: str
    category: str
    description: str
    difficulty: str


class ProjectSummary(BaseModel):
    name: str
    description: str
    difficulty: str


class CareerDetail(CareerSummary):
    skills: list[SkillSummary] = Field(default_factory=list)
    projects: list[ProjectSummary] = Field(default_factory=list)


class LearningPathItem(BaseModel):
    order: int
    name: str
    category: str
    description: str
    difficulty: str


class LearningPathResponse(BaseModel):
    career: str
    path: list[LearningPathItem]


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    description: str = ""
    difficulty: str = ""
    category: str = ""


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str


class GraphData(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class ConnectionStep(BaseModel):
    from_node: str
    to_node: str
    relationship: str
    from_type: str
    to_type: str


class ConnectionResponse(BaseModel):
    source: str
    target: str
    found: bool
    hops: int = 0
    path_nodes: list[str] = Field(default_factory=list)
    steps: list[ConnectionStep] = Field(default_factory=list)
    message: str = ""


class StatsResponse(BaseModel):
    careers: int
    skills: int
    relationships: int


class SearchResult(BaseModel):
    name: str
    type: str
    description: str


class HealthResponse(BaseModel):
    status: str
    database: str
    message: str = ""


class SkillDetail(SkillSummary):
    prerequisites: list[SkillSummary] = Field(default_factory=list)
    leads_to: list[SkillSummary] = Field(default_factory=list)
    related: list[SkillSummary] = Field(default_factory=list)
