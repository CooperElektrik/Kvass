import json
import sys
from .json_canvas.graph import CanvasGraph, TextNode, FileNode, GroupNode, LinkNode

class Interpreter:
    def __init__(self, story_graph: CanvasGraph):
        self.story_graph = story_graph
        self.next_steps = []
        self.start_nodes = self.story_graph.get_start_nodes()
        self.current_node = None

    def run(self):

        if not self.start_nodes: 
            return

        self.current_node = self.start_nodes[0]

        while self.current_node:
            if isinstance(self.current_node, TextNode):
                self.do_text(self.current_node.text)
            elif isinstance(self.current_node, FileNode):
                self.do_file(self.current_node.file)
            elif isinstance(self.current_node, LinkNode):
                self.do_link(self.current_node.url)
            elif isinstance(self.current_node, GroupNode):
                self.do_group(self.current_node.label)
            else:
                raise ValueError(f"Unknown node type: {self.current_node.type}")

            self.next_steps = self.story_graph.get_next_steps(self.current_node.id)

            if not self.next_steps:
                self.end()
                break

            if len(self.next_steps) == 1 and self.next_steps[0][0] is None:
                self.current_node = self.next_steps[0][1]
                continue

            self.do_choice(self.next_steps)

    def do_text(self, text):
        raise NotImplementedError("do_text not implemented")

    def do_file(self, file):
        raise NotImplementedError("do_file not implemented")

    def do_link(self, url):
        raise NotImplementedError("do_link not implemented")

    def do_group(self, label):
        raise NotImplementedError("do_group not implemented")

    def do_choice(self, choices):
        raise NotImplementedError("do_choice not implemented")

    def end(self):
        raise NotImplementedError("end not implemented")
    
class InteractiveInterpreter(Interpreter):
    def __init__(self, story_graph: CanvasGraph):
        super().__init__(story_graph)

    def do_text(self, text):
        print(text)

    def do_file(self, file):
        print(f"Opening file: {file}")

    def do_link(self, url):
        print(f"Opening link: {url}")

    def do_group(self, label):
        print(f"Entering group: {label}")

    def do_choice(self, choices):
        print("\nWhat do you do?")
        for i, (label, node) in enumerate(choices):
            choice_text = label
            print(f"  {i + 1}. {choice_text}")

        while True:
            try:
                choice_index = int(input("> ")) - 1
                if 0 <= choice_index < len(self.next_steps):
                    self.current_node = self.next_steps[choice_index][1]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def end(self):
        print("End of story.")

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