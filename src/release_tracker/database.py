from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from .config import get_settings

"""
The @lru_cache decorator on the get_engine() ensures that Python only ever 
executes this function once
On subsequent calls, it returns the exact same cached Engine object
"""


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_settings().database_url)


def get_session() -> Generator[Session]:
    with Session(get_engine()) as session:
        yield session
