from uuid import uuid4
from typing import TypeVar, Sequence, Optional

T = TypeVar("T")


def random_id() -> str:
    return str(uuid4()).replace("-", "")


def head_option(ls: Sequence[T]) -> Optional[T]:
    return ls[0] if ls else None
