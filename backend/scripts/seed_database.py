"""
Seed SkillGraph AI database with careers, skills, projects, and relationships.

Usage (from backend/ directory):
    python -m scripts.seed_database

Requires COGNODB_URI, COGNODB_USERNAME, COGNODB_PASSWORD in .env or environment.
"""

import sys
from pathlib import Path

# Allow running as `python -m scripts.seed_database` from backend/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.config import settings
from app.queries import CLEAR_DATABASE

# ---------------------------------------------------------------------------
# Node definitions
# ---------------------------------------------------------------------------

CAREERS = [
    {
        "name": "Frontend Developer",
        "description": "Builds user-facing web applications with modern JavaScript frameworks, focusing on performance, accessibility, and responsive design.",
        "category": "Software Engineering",
        "difficulty": "Intermediate",
    },
    {
        "name": "Backend Developer",
        "description": "Designs and implements server-side logic, APIs, and database integrations that power web and mobile applications.",
        "category": "Software Engineering",
        "difficulty": "Intermediate",
    },
    {
        "name": "Full Stack Developer",
        "description": "Works across the entire application stack — from UI components to APIs and databases — delivering end-to-end features.",
        "category": "Software Engineering",
        "difficulty": "Advanced",
    },
    {
        "name": "AI Engineer",
        "description": "Develops intelligent systems using machine learning, deep learning, and MLOps practices to solve complex data-driven problems.",
        "category": "Artificial Intelligence",
        "difficulty": "Advanced",
    },
    {
        "name": "Data Analyst",
        "description": "Extracts insights from data using statistical analysis, visualization, and SQL to support business decisions.",
        "category": "Data Science",
        "difficulty": "Intermediate",
    },
]

SKILLS = [
    {
        "name": "Programming Fundamentals",
        "category": "Foundation",
        "description": "Core concepts: variables, control flow, functions, data structures, and problem-solving.",
        "difficulty": "Beginner",
    },
    {
        "name": "HTML",
        "category": "Frontend",
        "description": "Markup language for structuring web content with semantic elements.",
        "difficulty": "Beginner",
    },
    {
        "name": "CSS",
        "category": "Frontend",
        "description": "Stylesheet language for layout, typography, and responsive design.",
        "difficulty": "Beginner",
    },
    {
        "name": "JavaScript",
        "category": "Frontend",
        "description": "Dynamic programming language for interactive web applications.",
        "difficulty": "Intermediate",
    },
    {
        "name": "TypeScript",
        "category": "Frontend",
        "description": "Typed superset of JavaScript that improves code quality and developer experience.",
        "difficulty": "Intermediate",
    },
    {
        "name": "React",
        "category": "Frontend",
        "description": "Component-based library for building user interfaces with a virtual DOM.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Advanced React",
        "category": "Frontend",
        "description": "Performance optimization, state management patterns, server components, and testing.",
        "difficulty": "Advanced",
    },
    {
        "name": "Python",
        "category": "Backend",
        "description": "Versatile language widely used for web development, data science, and automation.",
        "difficulty": "Intermediate",
    },
    {
        "name": "SQL",
        "category": "Database",
        "description": "Structured query language for relational database management and analytics.",
        "difficulty": "Intermediate",
    },
    {
        "name": "FastAPI",
        "category": "Backend",
        "description": "Modern Python web framework for building high-performance REST APIs.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Node.js",
        "category": "Backend",
        "description": "JavaScript runtime for building scalable server-side applications.",
        "difficulty": "Intermediate",
    },
    {
        "name": "REST APIs",
        "category": "Backend",
        "description": "Design principles for stateless HTTP-based application programming interfaces.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Git",
        "category": "DevOps",
        "description": "Version control system for tracking code changes and collaborating with teams.",
        "difficulty": "Beginner",
    },
    {
        "name": "Docker",
        "category": "DevOps",
        "description": "Containerization platform for packaging and deploying applications consistently.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Machine Learning",
        "category": "AI/ML",
        "description": "Algorithms and techniques for training models that learn patterns from data.",
        "difficulty": "Advanced",
    },
    {
        "name": "Deep Learning",
        "category": "AI/ML",
        "description": "Neural network architectures for complex pattern recognition and generative AI.",
        "difficulty": "Advanced",
    },
    {
        "name": "Statistics",
        "category": "Data Science",
        "description": "Mathematical methods for analyzing data distributions, hypothesis testing, and inference.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Pandas",
        "category": "Data Science",
        "description": "Python library for data manipulation, cleaning, and analysis with DataFrames.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Data Visualization",
        "category": "Data Science",
        "description": "Creating charts and dashboards to communicate data insights effectively.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Testing",
        "category": "Quality",
        "description": "Unit, integration, and end-to-end testing practices for reliable software.",
        "difficulty": "Intermediate",
    },
    {
        "name": "System Design",
        "category": "Architecture",
        "description": "Designing scalable, fault-tolerant distributed systems and microservices.",
        "difficulty": "Advanced",
    },
    {
        "name": "GraphQL",
        "category": "Backend",
        "description": "Query language and runtime for APIs that lets clients request exactly the data they need.",
        "difficulty": "Advanced",
    },
    {
        "name": "MongoDB",
        "category": "Database",
        "description": "Document-oriented NoSQL database for flexible schema designs.",
        "difficulty": "Intermediate",
    },
    {
        "name": "NumPy",
        "category": "Data Science",
        "description": "Fundamental Python library for numerical computing and array operations.",
        "difficulty": "Intermediate",
    },
    {
        "name": "AWS Basics",
        "category": "Cloud",
        "description": "Core Amazon Web Services: EC2, S3, Lambda, and cloud deployment fundamentals.",
        "difficulty": "Intermediate",
    },
]

PROJECTS = [
    {
        "name": "Portfolio Website",
        "description": "A responsive personal portfolio showcasing projects and skills built with HTML, CSS, and JavaScript.",
        "difficulty": "Beginner",
    },
    {
        "name": "React Dashboard",
        "description": "Interactive admin dashboard with charts, tables, and real-time data using React and TypeScript.",
        "difficulty": "Intermediate",
    },
    {
        "name": "REST API",
        "description": "Production-ready REST API with authentication, validation, and database integration.",
        "difficulty": "Intermediate",
    },
    {
        "name": "AI Resume Builder",
        "description": "ML-powered application that analyzes resumes and suggests improvements using NLP.",
        "difficulty": "Advanced",
    },
    {
        "name": "Data Dashboard",
        "description": "Business intelligence dashboard with SQL queries, Pandas processing, and interactive visualizations.",
        "difficulty": "Intermediate",
    },
    {
        "name": "E-commerce Frontend",
        "description": "Full-featured online store UI with product catalog, cart, and checkout flow.",
        "difficulty": "Advanced",
    },
    {
        "name": "ML Classification Model",
        "description": "End-to-end machine learning pipeline for image or text classification with model evaluation.",
        "difficulty": "Advanced",
    },
    {
        "name": "DevOps Pipeline",
        "description": "CI/CD pipeline with Docker containers, automated testing, and cloud deployment.",
        "difficulty": "Advanced",
    },
    {
        "name": "Blog Platform",
        "description": "Full stack blog with user authentication, markdown editor, and comment system.",
        "difficulty": "Intermediate",
    },
    {
        "name": "Analytics Report Generator",
        "description": "Automated report tool that queries databases and produces PDF/visual summaries.",
        "difficulty": "Intermediate",
    },
]

# (from_label, relationship, to_label) — labels are node names
RELATIONSHIPS = [
    # PREREQUISITE_OF chains — Frontend
    ("Programming Fundamentals", "PREREQUISITE_OF", "HTML"),
    ("Programming Fundamentals", "PREREQUISITE_OF", "JavaScript"),
    ("Programming Fundamentals", "PREREQUISITE_OF", "Python"),
    ("Programming Fundamentals", "PREREQUISITE_OF", "Git"),
    ("HTML", "PREREQUISITE_OF", "CSS"),
    ("CSS", "PREREQUISITE_OF", "JavaScript"),
    ("JavaScript", "PREREQUISITE_OF", "React"),
    ("JavaScript", "PREREQUISITE_OF", "Node.js"),
    ("JavaScript", "PREREQUISITE_OF", "TypeScript"),
    ("React", "PREREQUISITE_OF", "Advanced React"),
    ("TypeScript", "PREREQUISITE_OF", "Advanced React"),
    # Backend chain
    ("Python", "PREREQUISITE_OF", "FastAPI"),
    ("Python", "PREREQUISITE_OF", "Pandas"),
    ("Python", "PREREQUISITE_OF", "Machine Learning"),
    ("SQL", "PREREQUISITE_OF", "REST APIs"),
    ("FastAPI", "PREREQUISITE_OF", "REST APIs"),
    ("REST APIs", "PREREQUISITE_OF", "GraphQL"),
    ("REST APIs", "PREREQUISITE_OF", "System Design"),
    # Data / ML chain
    ("Statistics", "PREREQUISITE_OF", "Pandas"),
    ("Statistics", "PREREQUISITE_OF", "Machine Learning"),
    ("NumPy", "PREREQUISITE_OF", "Pandas"),
    ("NumPy", "PREREQUISITE_OF", "Machine Learning"),
    ("Pandas", "PREREQUISITE_OF", "Data Visualization"),
    ("Pandas", "PREREQUISITE_OF", "Machine Learning"),
    ("Machine Learning", "PREREQUISITE_OF", "Deep Learning"),
    ("SQL", "PREREQUISITE_OF", "Data Visualization"),
    # DevOps
    ("Git", "PREREQUISITE_OF", "Docker"),
    ("Docker", "PREREQUISITE_OF", "AWS Basics"),
    ("Testing", "PREREQUISITE_OF", "System Design"),
    # RELATED_TO — cross-connections for path finding
    ("React", "RELATED_TO", "Node.js"),
    ("TypeScript", "RELATED_TO", "FastAPI"),
    ("SQL", "RELATED_TO", "MongoDB"),
    ("GraphQL", "RELATED_TO", "REST APIs"),
    ("Machine Learning", "RELATED_TO", "Data Visualization"),
    ("Python", "RELATED_TO", "JavaScript"),
    ("Docker", "RELATED_TO", "AWS Basics"),
    ("Pandas", "RELATED_TO", "SQL"),
    ("Testing", "RELATED_TO", "Git"),
    ("Advanced React", "RELATED_TO", "System Design"),
    # Career REQUIRES skills
    ("Frontend Developer", "REQUIRES", "HTML"),
    ("Frontend Developer", "REQUIRES", "CSS"),
    ("Frontend Developer", "REQUIRES", "JavaScript"),
    ("Frontend Developer", "REQUIRES", "React"),
    ("Frontend Developer", "REQUIRES", "TypeScript"),
    ("Frontend Developer", "REQUIRES", "Git"),
    ("Backend Developer", "REQUIRES", "Python"),
    ("Backend Developer", "REQUIRES", "SQL"),
    ("Backend Developer", "REQUIRES", "FastAPI"),
    ("Backend Developer", "REQUIRES", "REST APIs"),
    ("Backend Developer", "REQUIRES", "Docker"),
    ("Backend Developer", "REQUIRES", "Git"),
    ("Full Stack Developer", "REQUIRES", "JavaScript"),
    ("Full Stack Developer", "REQUIRES", "React"),
    ("Full Stack Developer", "REQUIRES", "Node.js"),
    ("Full Stack Developer", "REQUIRES", "SQL"),
    ("Full Stack Developer", "REQUIRES", "REST APIs"),
    ("Full Stack Developer", "REQUIRES", "System Design"),
    ("Full Stack Developer", "REQUIRES", "Git"),
    ("AI Engineer", "REQUIRES", "Python"),
    ("AI Engineer", "REQUIRES", "Machine Learning"),
    ("AI Engineer", "REQUIRES", "Deep Learning"),
    ("AI Engineer", "REQUIRES", "Statistics"),
    ("AI Engineer", "REQUIRES", "Pandas"),
    ("AI Engineer", "REQUIRES", "Docker"),
    ("Data Analyst", "REQUIRES", "SQL"),
    ("Data Analyst", "REQUIRES", "Statistics"),
    ("Data Analyst", "REQUIRES", "Pandas"),
    ("Data Analyst", "REQUIRES", "Data Visualization"),
    ("Data Analyst", "REQUIRES", "Python"),
    # Career RECOMMENDS_PROJECT
    ("Frontend Developer", "RECOMMENDS_PROJECT", "Portfolio Website"),
    ("Frontend Developer", "RECOMMENDS_PROJECT", "React Dashboard"),
    ("Frontend Developer", "RECOMMENDS_PROJECT", "E-commerce Frontend"),
    ("Backend Developer", "RECOMMENDS_PROJECT", "REST API"),
    ("Backend Developer", "RECOMMENDS_PROJECT", "DevOps Pipeline"),
    ("Full Stack Developer", "RECOMMENDS_PROJECT", "Blog Platform"),
    ("Full Stack Developer", "RECOMMENDS_PROJECT", "E-commerce Frontend"),
    ("AI Engineer", "RECOMMENDS_PROJECT", "AI Resume Builder"),
    ("AI Engineer", "RECOMMENDS_PROJECT", "ML Classification Model"),
    ("Data Analyst", "RECOMMENDS_PROJECT", "Data Dashboard"),
    ("Data Analyst", "RECOMMENDS_PROJECT", "Analytics Report Generator"),
    # Project USES skills
    ("Portfolio Website", "USES", "HTML"),
    ("Portfolio Website", "USES", "CSS"),
    ("Portfolio Website", "USES", "JavaScript"),
    ("React Dashboard", "USES", "React"),
    ("React Dashboard", "USES", "TypeScript"),
    ("REST API", "USES", "Python"),
    ("REST API", "USES", "FastAPI"),
    ("REST API", "USES", "SQL"),
    ("AI Resume Builder", "USES", "Python"),
    ("AI Resume Builder", "USES", "Machine Learning"),
    ("AI Resume Builder", "USES", "Deep Learning"),
    ("Data Dashboard", "USES", "SQL"),
    ("Data Dashboard", "USES", "Pandas"),
    ("Data Dashboard", "USES", "Data Visualization"),
    ("E-commerce Frontend", "USES", "React"),
    ("E-commerce Frontend", "USES", "TypeScript"),
    ("E-commerce Frontend", "USES", "REST APIs"),
    ("ML Classification Model", "USES", "Python"),
    ("ML Classification Model", "USES", "Machine Learning"),
    ("ML Classification Model", "USES", "Pandas"),
    ("DevOps Pipeline", "USES", "Docker"),
    ("DevOps Pipeline", "USES", "Git"),
    ("DevOps Pipeline", "USES", "Testing"),
    ("Blog Platform", "USES", "React"),
    ("Blog Platform", "USES", "Node.js"),
    ("Blog Platform", "USES", "MongoDB"),
    ("Analytics Report Generator", "USES", "SQL"),
    ("Analytics Report Generator", "USES", "Pandas"),
    ("Analytics Report Generator", "USES", "Data Visualization"),
]

CREATE_CAREER = """
CREATE (c:Career {
    name: $name,
    description: $description,
    category: $category,
    difficulty: $difficulty
})
"""

CREATE_SKILL = """
CREATE (s:Skill {
    name: $name,
    category: $category,
    description: $description,
    difficulty: $difficulty
})
"""

CREATE_PROJECT = """
CREATE (p:Project {
    name: $name,
    description: $description,
    difficulty: $difficulty
})
"""

CREATE_RELATIONSHIP = """
MATCH (a {name: $from_name})
MATCH (b {name: $to_name})
CREATE (a)-[r:%s]->(b)
RETURN type(r) AS rel_type
"""


def seed_database() -> None:
    driver = GraphDatabase.driver(
        settings.cognodb_uri,
        auth=(settings.cognodb_username, settings.cognodb_password),
    )

    try:
        driver.verify_connectivity()
        print("Connected to CognoDB.")

        with driver.session() as session:
            print("Clearing existing data...")
            session.run(CLEAR_DATABASE)

            print(f"Creating {len(CAREERS)} careers...")
            for career in CAREERS:
                session.run(CREATE_CAREER, **career)

            print(f"Creating {len(SKILLS)} skills...")
            for skill in SKILLS:
                session.run(CREATE_SKILL, **skill)

            print(f"Creating {len(PROJECTS)} projects...")
            for project in PROJECTS:
                session.run(CREATE_PROJECT, **project)

            print(f"Creating {len(RELATIONSHIPS)} relationships...")
            for from_name, rel_type, to_name in RELATIONSHIPS:
                query = CREATE_RELATIONSHIP % rel_type
                session.run(query, from_name=from_name, to_name=to_name)

            # Verify counts
            result = session.run(
                """
                MATCH (c:Career) WITH count(c) AS careers
                MATCH (s:Skill) WITH careers, count(s) AS skills
                MATCH (p:Project) WITH careers, skills, count(p) AS projects
                MATCH ()-[r]->() RETURN careers, skills, projects, count(r) AS rels
                """
            )
            record = result.single()
            print("\nSeed complete!")
            print(f"  Careers:       {record['careers']}")
            print(f"  Skills:        {record['skills']}")
            print(f"  Projects:      {record['projects']}")
            print(f"  Relationships: {record['rels']}")

    except ServiceUnavailable as exc:
        print(f"ERROR: Cannot connect to CognoDB — {exc}")
        sys.exit(1)
    except Neo4jError as exc:
        print(f"ERROR: Database error — {exc}")
        sys.exit(1)
    finally:
        driver.close()


if __name__ == "__main__":
    seed_database()
