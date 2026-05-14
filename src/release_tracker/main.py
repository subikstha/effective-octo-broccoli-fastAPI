from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlmodel import Session, select

from .database import get_session
from .models import Project, ProjectCreate, ProjectRead, ProjectUpdate


def slugify(value: str) -> str:
    cleaned = "".join(c for c in value.lower() if c.isalnum() or c == " ")
    return "-".join(cleaned.split()) or "project"


app = FastAPI(
    title="Release Tracker API",
    description="An API for tracking project milestones and tasks for devs",
)

"""
Creates a reusable FastAPI dependency alias
This packages database session coming from get_session() into a SessionDep name
Whenever you see SessionDep, FastAPI should inject a database session using get_session()
Replaces this
def get_projects(session: Session = Depends(get_session)):
"""
SessionDep = Annotated[
    Session, Depends(get_session)
]  # Means everytime you need the Session use the get_session()


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
    statement = select(Project).order_by(Project.name)
    projects = session.exec(statement).all()  # Execute this statement
    # if session.exec(statement).one() is used and no result is found , it will throw an exception
    # or throw an exception if more than one result is found
    return list(projects)  # Ensuring that a list is returned


@app.post(
    "/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
def create_project(payload: ProjectCreate, session: SessionDep):
    project = Project.model_validate(
        payload, update={"slug": slugify(payload.name)}
    )  # Creates project model instance from ProjectCreate payload
    # update is used to inject additional fields in the payload that is not originally there

    session.add(project)
    session.commit()
    session.refresh(project)  # Doing this we get the PK set in the DB

    return project


@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, payload: ProjectCreate, session: SessionDep
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not foun"
        )
    updated_fields = project.model_dump(
        exclude_unset=True
    )  # Only get those fields which have been changed
    project.sqlmodel_update(
        updated_fields
    )  # update the project with new fields and make sure it is validated

    if "name" in updated_fields and updated_fields["name"] is not None:
        project.slug = slugify(updated_fields["name"])

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    session.delete(project)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
