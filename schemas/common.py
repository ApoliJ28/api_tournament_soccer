from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    skip: int
    limit: int
    total: int
    page: int
    limit: int
    pages: int
    payload: List[T]
