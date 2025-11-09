from typing import Optional
from dataclasses import dataclass


@dataclass
class Node:
    id: str
    type: str
    x: int
    y: int
    width: int
    height: int
    color: Optional[str] = None


@dataclass
class TextNode(Node):
    text: str = ""


@dataclass
class FileNode(Node):
    file: str = ""
    subpath: Optional[str] = None