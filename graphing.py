from python_call_trace import PythonCallTrace
from flow_node import FlowNode
from graphviz import Digraph


class GraphBuilder:
    def __init__(
        self,
        comment: str,
        flow_analyzer: PythonCallTrace,
    ):
        self.dot = Digraph(comment=comment)
        self.flow_analyzer = flow_analyzer
        self.visited = set()

    def add_nodes_edges(self, node: FlowNode):
        if node.id in self.visited:
            return
        self.visited.add(node.id)

        styles = {
            "ENTRY": {
                "shape": "ellipse",
                "style": "filled",
                "fillcolor": "lightgreen",
            },
            "FUNCTION": {
                "shape": "box",
                "style": "filled",
                "fillcolor": "lightblue",
            },
            "CONDITION": {
                "shape": "diamond",
                "style": "filled",
                "fillcolor": "lightyellow",
            },
            "CALL": {"shape": "box", "style": "filled", "fillcolor": "lightpink"},
            "MERGE": {
                "shape": "circle",
                "style": "filled",
                "fillcolor": "lightgray",
            },
            "END": {
                "shape": "ellipse",
                "style": "filled",
                "fillcolor": "lightgreen",
            },
        }

        style = styles.get(node.type, {"shape": "box"})
        self.dot.node(node.id, node.label, **style)

        for child in node.children:
            self.dot.edge(node.id, child.id)
            self.add_nodes_edges(child)

    def create_visual_graph(self, output_file: str):
        """Create a visual representation of the execution flow graph"""
        self.dot.attr(rankdir="TB")

        if self.flow_analyzer.entry_node is None:
            raise ValueError(
                "No Entry Node found which infers no 'main' function present in file"
            )

        self.add_nodes_edges(self.flow_analyzer.entry_node)
        self.dot.render(output_file, view=True, format="png")
