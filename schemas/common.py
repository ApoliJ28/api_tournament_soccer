from typing import List, Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginatedResponse(GenericModel, Generic[T]):
    skip: int
    limit: int
    total: int
    page: int
    limit: int
    pages: int
    payload: List[T]
