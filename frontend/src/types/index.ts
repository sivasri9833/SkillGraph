export interface Career {
  name: string;
  description: string;
  category: string;
  difficulty: string;
}

export interface Skill {
  name: string;
  category: string;
  description: string;
  difficulty: string;
}

export interface Project {
  name: string;
  description: string;
  difficulty: string;
}

export interface CareerDetail extends Career {
  skills: Skill[];
  projects: Project[];
}

export interface LearningPathItem {
  order: number;
  name: string;
  category: string;
  description: string;
  difficulty: string;
}

export interface LearningPath {
  career: string;
  path: LearningPathItem[];
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  description?: string;
  difficulty?: string;
  category?: string;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface ConnectionStep {
  from_node: string;
  to_node: string;
  relationship: string;
  from_type: string;
  to_type: string;
}

export interface ConnectionResult {
  source: string;
  target: string;
  found: boolean;
  hops: number;
  path_nodes: string[];
  steps: ConnectionStep[];
  message: string;
}

export interface Stats {
  careers: number;
  skills: number;
  relationships: number;
}

export interface SearchResult {
  name: string;
  type: string;
  description: string;
}

export interface HealthStatus {
  status: string;
  database: string;
  message?: string;
}

export interface SkillDetail extends Skill {
  prerequisites: Skill[];
  leads_to: Skill[];
  related: Skill[];
}
