from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

StringConstraints(strip_whitespace=True, min_length=2, max_length=120)

StrippedName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=2, max_length=120)
]


# Pydantic model example
class ProjectCreate(BaseModel):
    name: StrippedName
    description: str | None = Field(default=None, max_length=1000)


@dataclass
class Project:
    name: str
    archived: bool = False

    def archive(self) -> None:
        self.archived = True


def validate_project_name(name: str) -> str:
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("Project name cannot be blank")
    return cleaned


try:
    valid_project_name = validate_project_name("")
except ValueError:
    valid_project_name = "DEFAULT"

# Context manager to read files
with open("tasks.txt") as f:
    contents = f.read()


# This is a decorator example
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@log_call
def normalize_title(title):
    return title.strip().title()
