from fastapi import FastAPI, HTTPException, status

from . import crud
from .dependencies import SessionDep
from .models import Project, ProjectCreate, ProjectRead, ProjectUpdate


def slugify(value: str) -> str:
    cleaned = "".join(c for c in value.lower() if c.isalnum() or c == " ")
    return "-".join(cleaned.split()) or "project"


app = FastAPI(
    title="Release Tracker API",
    description="An API for tracking project milestones and tasks for devs",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Release Tracker", "docs": "/docs"}


"""
Creates a reusable FastAPI dependency alias
This packages database session coming from get_session() into a SessionDep name
Whenever you see SessionDep, FastAPI should inject a database session using get_session()
Replaces this
def get_projects(session: Session = Depends(get_session)):
"""


@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)  # Fetch one row of the DB by PK
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return project


"""
specifying response_model, FastAPI automatically takes the Project database models
returned by session.exec() and validates them against our ProjectRead schema
and serializes them to JSON
"""


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(session: SessionDep):
    return crud.list_projects(session)


@app.post(
    "/projects", response_model=Project, status_code=status.HTTP_201_CREATED
)
def create_project(payload: ProjectCreate, session: SessionDep):
    return crud.create_project(payload=payload, session=session)


@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, payload: ProjectUpdate, session: SessionDep
):
    project = crud.get_project_by_id(session, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return crud.update_project(session, project, payload)


@app.get("/projects/{project_id}", status_code=status.HTTP_200_OK)
def get_project_by_id(project_id: int, session: SessionDep):
    project = crud.get_project_by_id(session, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep):
    project = crud.get_project_by_id(session, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return crud.delete_project(session, project)
