from contextlib import asynccontextmanager
from typing import Any, Generator

from fastapi import FastAPI
from neo4j import Driver, GraphDatabase, Session
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.config import settings

_driver: Driver | None = None


def get_driver() -> Driver:
    if _driver is None:
        raise RuntimeError("Database driver is not initialized.")
    return _driver


def get_session() -> Generator[Session, None, None]:
    """Yield a Neo4j session for dependency injection."""
    driver = get_driver()
    session = driver.session()
    try:
        yield session
    finally:
        session.close()


def init_driver() -> None:
    global _driver
    _driver = GraphDatabase.driver(
        settings.cognodb_uri,
        auth=(settings.cognodb_username, settings.cognodb_password),
    )
    _driver.verify_connectivity()


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def check_connectivity() -> dict[str, Any]:
    """Verify database connectivity for health checks."""
    try:
        driver = get_driver()
        driver.verify_connectivity()
        with driver.session() as session:
            result = session.run("RETURN 1 AS ok")
            record = result.single()
            if record and record["ok"] == 1:
                return {"status": "connected"}
        return {"status": "error", "message": "Unexpected database response."}
    except ServiceUnavailable:
        return {"status": "unavailable", "message": "Database service is unavailable."}
    except Neo4jError as exc:
        return {"status": "error", "message": "Database connection failed."}
    except RuntimeError:
        return {"status": "unavailable", "message": "Database driver is not initialized."}


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_driver()
    yield
    close_driver()
