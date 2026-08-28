import type {
  Career,
  CareerDetail,
  ConnectionResult,
  GraphData,
  HealthStatus,
  LearningPath,
  SearchResult,
  Skill,
  SkillDetail,
  Stats,
} from '../types';

// const API_BASE = import.meta.env.VITE_API_URL || '';
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (body.detail) detail = body.detail;
    } catch {
      // ignore parse errors
    }
    throw new ApiError(detail, response.status);
  }
  return response.json();
}

export const api = {
  health: () => fetchJson<HealthStatus>('/api/health'),

  getCareers: () => fetchJson<Career[]>('/api/careers'),

  getCareer: (name: string) =>
    fetchJson<CareerDetail>(`/api/careers/${encodeURIComponent(name)}`),

  getLearningPath: (name: string) =>
    fetchJson<LearningPath>(
      `/api/careers/${encodeURIComponent(name)}/learning-path`,
    ),

  getSkills: () => fetchJson<Skill[]>('/api/skills'),

  getSkill: (name: string) =>
    fetchJson<SkillDetail>(`/api/skills/${encodeURIComponent(name)}`),

  getStats: () => fetchJson<Stats>('/api/careers/stats/summary'),

  search: (query: string) =>
    fetchJson<SearchResult[]>(
      `/api/careers/search?q=${encodeURIComponent(query)}`,
    ),

  getCareerGraph: (name: string) =>
    fetchJson<GraphData>(
      `/api/graph/career/${encodeURIComponent(name)}`,
    ),

  getConnections: (source: string, target: string) =>
    fetchJson<ConnectionResult>(
      `/api/graph/connections?source=${encodeURIComponent(source)}&target=${encodeURIComponent(target)}`,
    ),
};

export { ApiError };
