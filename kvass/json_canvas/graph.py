from collections import defaultdict
from typing import List, Dict, Optional, Any, Tuple
from .nodes import Node, TextNode, FileNode
from .edges import Edge

NODE_TYPE_MAP = {
    "text": TextNode,
    "file": FileNode,
}


class CanvasGraph:
    def __init__(self, canvas_data: Dict[str, Any]):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self._adjacency_list: Dict[str, List[Edge]] = defaultdict(list)

        self._parse(canvas_data)

    def _parse(self, canvas_data: Dict[str, Any]):
        raw_nodes = canvas_data.get("nodes", [])
        raw_edges = canvas_data.get("edges", [])

        for node_data in raw_nodes:
            node_type = node_data.get("type")
            node_class = NODE_TYPE_MAP.get(node_type)
            node = node_class(**node_data)
            self.nodes[node.id] = node

        for edge_data in raw_edges:
            edge = Edge(**edge_data)
            self.edges.append(edge)
            self._adjacency_list[edge.fromNode].append(edge)

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def get_start_nodes(self) -> List[Node]:
        """
        Finds all nodes that are potential starts.
        A start node is any node that is not a destination for any edge.
        """
        destination_node_ids = {edge.toNode for edge in self.edges}
        return [
            node
            for node_id, node in self.nodes.items()
            if node_id not in destination_node_ids
        ]

    def get_next_steps(self, current_node_id: str) -> List[Tuple[Optional[str], Node]]:
        """
        Given a node ID, returns a list of possible next steps.
        Each step is a tuple: (choice_label, destination_node).
        The choice_label is the edge's label, or None if not a choice.
        """
        steps = []
        outgoing_edges = self._adjacency_list.get(current_node_id, [])
        for edge in outgoing_edges:
            destination_node = self.get_node(edge.toNode)
            if destination_node:
                steps.append((edge.label, destination_node))
        return steps
