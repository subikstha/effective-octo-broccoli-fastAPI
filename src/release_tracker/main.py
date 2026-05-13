from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Release Tracker API")


class ProjectRead(BaseModel):
    id: int
    name: str
    slug: str


@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int):
    return mock_database.get(
        project_id
    )  # This will return None if the id is not found instead of using mock_database[project_id] which would raise a KeyError


@app.get("/projects")
def list_projects(name: str | None = None):
    projects = list(mock_database.values())
    if name is None:
        return projects
    return [p for p in projects if p.name == name]


# A simple mock database for now
mock_database: dict[int, ProjectRead] = {
    1: ProjectRead(id=1, name="Frontend Redesign", slug="frontend-redesign"),
    2: ProjectRead(id=2, name="API v2", slug="api-v2"),
    3: ProjectRead(id=3, name="Database Migration", slug="database-migration"),
}
