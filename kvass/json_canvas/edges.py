from typing import Optional
from dataclasses import dataclass


@dataclass
class Edge:
    id: str
    fromNode: str
    toNode: str
    label: Optional[str] = None
    color: Optional[str] = None
    fromSide: Optional[str] = None
    fromEnd: Optional[str] = None
    toSide: Optional[str] = None
    toEnd: Optional[str] = None
