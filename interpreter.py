import json
import sys
from time import sleep
from typing import Optional, List, Tuple
try:
    from .json_canvas.graph import CanvasGraph, TextNode, FileNode, GroupNode, LinkNode, Node
except ImportError:
    from json_canvas.graph import CanvasGraph, TextNode, FileNode, GroupNode, LinkNode, Node

class Interpreter:
    """
    Kvass interpreter.
    """

    def __init__(self, graph: CanvasGraph):
        self.graph = graph 
        self.current_node: Optional[Node] = None 
        self.is_started: bool = False 
        self.is_waiting_for_choice: bool = False
        self.is_finished: bool = False
        self.available_choices: List[Tuple[str, Node]] = []

    def start(self, node_id: str | None = None):
        if node_id:
            start_node = self.graph.get_node(node_id)
            if not start_node:
                raise ValueError(f"Cannot start: Node with ID '{node_id}' not found.")
            self.current_node = start_node
        else:
            start_nodes = self.graph.get_start_nodes()
            if not start_nodes:
                raise RuntimeError("Cannot start: No start nodes found in the story graph.")
            self.current_node = start_nodes[0]
            
        self.is_started = True
        self.is_finished = False
        self.is_waiting_for_choice = False
        self.step()

    def step(self):
        while self.current_node and not self.is_waiting_for_choice and not self.is_finished:

            self.on_node_enter(self.current_node)

            if isinstance(self.current_node, TextNode):
                self.do_text(self.current_node)
            elif isinstance(self.current_node, FileNode):
                self.do_file(self.current_node)
            elif isinstance(self.current_node, LinkNode):
                self.do_link(self.current_node)
            elif isinstance(self.current_node, GroupNode):
                self.do_group(self.current_node)
            else:
                raise ValueError(f"Unknown node type: {type(self.current_node)}")

            self.on_node_exit(self.current_node)

            next_steps = self.graph.get_next_steps(self.current_node.id)

            if not next_steps:
                self.is_finished = True
                self.end()
                self.current_node = None
                break

            if len(next_steps) == 1 and next_steps[0][0] is None:
                self.current_node = next_steps[0][1]

            else:
                self.available_choices = next_steps
                self.is_waiting_for_choice = True
                self.do_choice(self.available_choices)
            
            break
    
    def make_choice(self, choice_index: int):
        if not self.is_waiting_for_choice:
            return

        if not (0 <= choice_index < len(self.available_choices)):
            raise IndexError(f"Invalid choice index: {choice_index}")

        _, next_node = self.available_choices[choice_index]
        self.current_node = next_node
        
        self.is_waiting_for_choice = False
        self.available_choices = []
        
        self.step()

    def on_node_enter(self, node: Node):
        pass

    def on_node_exit(self, node: Node):
        pass

    def do_text(self, node: TextNode):
        raise NotImplementedError("do_text not implemented")

    def do_file(self, node: FileNode):
        raise NotImplementedError("do_file not implemented")

    def do_link(self, node: LinkNode):
        raise NotImplementedError("do_link not implemented")

    def do_group(self, node: GroupNode):
        raise NotImplementedError("do_group not implemented")

    def do_choice(self, choices: List[Tuple[str, Node]]):
        raise NotImplementedError("do_choice not implemented")

    def end(self):
        raise NotImplementedError("end not implemented")
    
    def run(self):
        raise NotImplementedError("run not implemented")


class InteractiveInterpreter(Interpreter):
    def do_text(self, node: TextNode):
        print(f"TEXT: {node.text}")

    def do_file(self, node: FileNode):
        print(f"FILE: {node.file}")

    def do_link(self, node: LinkNode):
        print(f"LINK: {node.url}")

    def do_group(self, node: GroupNode):
        print(f"GROUP: {node.label}")

    def do_choice(self, choices: List[Tuple[str, Node]]):
        print("\nMake a choice:")
        for i, (label, _) in enumerate(choices):
            print(f"{i + 1}. {label}")
        
        while True:
            try:
                choice_input = input("> ")
                choice_index = int(choice_input) - 1
                if 0 <= choice_index < len(choices):
                    self.make_choice(choice_index)
                    break
                else:
                    print("Invalid choice number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def end(self):
        print("\n--- End of story ---")

    def run(self, start_node_id: str | None = None):
        self.start(start_node_id)
        while not self.is_finished:
            sleep(1)
            if self.is_waiting_for_choice:
                self.do_choice(self.available_choices)
            else:
                self.step()
                


if __name__ == "__main__":
    try:
        canvas_data = open(sys.argv[1], "r").read()
    except IndexError:
        print("Use: python -m interpreter FILEPATH")
        exit()

    canvas_data = json.loads(canvas_data)
    graph = CanvasGraph(canvas_data)
    interpreter = InteractiveInterpreter(graph)
    interpreter.run()