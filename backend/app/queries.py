"""
Parameterized Cypher queries for SkillGraph AI.

All queries use driver parameters — never string-concatenate user input.
"""

# ---------------------------------------------------------------------------
# Query 1: Get Career Details
# Find a career and its directly required skills, recommended projects.
# ---------------------------------------------------------------------------
GET_CAREER_DETAILS = """
MATCH (c:Career {name: $career_name})
OPTIONAL MATCH (c)-[:REQUIRES]->(s:Skill)
OPTIONAL MATCH (c)-[:RECOMMENDS_PROJECT]->(p:Project)
RETURN c,
       collect(DISTINCT s) AS skills,
       collect(DISTINCT p) AS projects
"""

# ---------------------------------------------------------------------------
# Query 2: Multi-hop Learning Path
# Traverse PREREQUISITE_OF chains to order skills from foundation to advanced.
# For each skill required by the career, walk prerequisite chains up to 5 hops.
# ---------------------------------------------------------------------------
GET_LEARNING_PATH = """
MATCH (c:Career {name: $career_name})-[:REQUIRES]->(target:Skill)
OPTIONAL MATCH path = (foundation:Skill)-[:PREREQUISITE_OF*1..5]->(target)
WITH target, path
WITH target,
     CASE WHEN path IS NULL THEN [] ELSE nodes(path) END AS path_nodes
UNWIND CASE WHEN size(path_nodes) = 0 THEN [target] ELSE path_nodes END AS node
WITH DISTINCT node
RETURN node.name AS name,
       node.category AS category,
       node.description AS description,
       node.difficulty AS difficulty,
       length((node)-[:PREREQUISITE_OF*]->()) AS depth
ORDER BY depth ASC, name ASC
"""

# Alternative learning path that also includes skills with no prerequisites
GET_LEARNING_PATH_FULL = """
MATCH (c:Career {name: $career_name})-[:REQUIRES]->(required:Skill)
OPTIONAL MATCH prereq_path = (foundation:Skill)-[:PREREQUISITE_OF*1..5]->(required)
WITH required, prereq_path
WITH required,
     CASE WHEN prereq_path IS NULL THEN [required]
          ELSE nodes(prereq_path) END AS chain_nodes
UNWIND chain_nodes AS node
WITH DISTINCT node
RETURN node.name AS name,
       node.category AS category,
       node.description AS description,
       node.difficulty AS difficulty,
       size([(node)<-[:PREREQUISITE_OF*]-(ancestor:Skill) | ancestor]) AS depth
ORDER BY depth DESC, node.difficulty ASC, name ASC
"""

# ---------------------------------------------------------------------------
# Query 3: Find Connections Between Skills
# Shortest undirected path between two skills (up to 6 hops).
# ---------------------------------------------------------------------------
FIND_SKILL_CONNECTION = """
MATCH (source:Skill {name: $source_name}), (target:Skill {name: $target_name})
MATCH path = shortestPath((source)-[*..6]-(target))
RETURN path
"""

# List all careers
LIST_CAREERS = """
MATCH (c:Career)
RETURN c.name AS name,
       c.description AS description,
       c.category AS category,
       c.difficulty AS difficulty
ORDER BY c.name
"""

# List all skills
LIST_SKILLS = """
MATCH (s:Skill)
RETURN s.name AS name,
       s.category AS category,
       s.description AS description,
       s.difficulty AS difficulty
ORDER BY s.name
"""

# Dashboard statistics
GET_STATS = """
MATCH (c:Career)
WITH count(c) AS careers
MATCH (s:Skill)
WITH careers, count(s) AS skills
MATCH ()-[r]->()
RETURN careers, skills, count(r) AS relationships
"""

# Search careers and skills by name (case-insensitive partial match)
SEARCH_NODES = """
CALL {
  MATCH (c:Career)
  WHERE toLower(c.name) CONTAINS toLower($query)
  RETURN c.name AS name, 'career' AS type, c.description AS description
  UNION
  MATCH (s:Skill)
  WHERE toLower(s.name) CONTAINS toLower($query)
  RETURN s.name AS name, 'skill' AS type, s.description AS description
}
RETURN name, type, description
ORDER BY name
LIMIT 20
"""

# Graph data for career explorer visualization
GET_CAREER_GRAPH = """
MATCH (c:Career {name: $career_name})
OPTIONAL MATCH (c)-[:REQUIRES]->(s:Skill)
WITH c, collect(DISTINCT s) AS skills
UNWIND skills AS s
OPTIONAL MATCH (s)-[r:PREREQUISITE_OF|RELATED_TO]->(related:Skill)
WHERE related IN skills
WITH c, skills,
     collect(DISTINCT {
       source: s.name,
       target: related.name,
       type: type(r)
     }) AS skill_relationships
RETURN c, skills, skill_relationships
"""

# Get single skill details with related skills
GET_SKILL_DETAILS = """
MATCH (s:Skill {name: $skill_name})
OPTIONAL MATCH (s)-[:PREREQUISITE_OF]->(advanced:Skill)
OPTIONAL MATCH (prereq:Skill)-[:PREREQUISITE_OF]->(s)
OPTIONAL MATCH (s)-[:RELATED_TO]-(related:Skill)
RETURN s,
       collect(DISTINCT prereq) AS prerequisites,
       collect(DISTINCT advanced) AS leads_to,
       collect(DISTINCT related) AS related
"""

# Clear all data (used by seed script)
CLEAR_DATABASE = """
MATCH (n) DETACH DELETE n
"""
