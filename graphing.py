from python_call_trace import PythonCallTrace
from flow_node import FlowNode
from graphviz import Digraph


class GraphBuilder:
    def __init__(
        self,
        comment: str,
        call_tracer: PythonCallTrace,
    ):
        self.dot = Digraph(comment=comment)
        self.call_tracer = call_tracer
        self.visited = set()

    def add_nodes_edges(self, node: FlowNode):
        """Add nodes and edges to the graph"""
        # Check if node is already visited
        if node.id in self.visited:
            return
        self.visited.add(node.id)

        # Define different styles for different node types to use in GraphViz
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
            "CALL": {"shape": "box", "style": "filled", "fillcolor": "lightpink"},
            "LOOP": {
                "shape": "ellipse",
                "style": "filled",
                "fillcolor": "lightgray",
            },
            "CONDITION": {
                "shape": "diamond",
                "style": "filled",
                "fillcolor": "lightgray",
            },
            "END_IF": {
                "shape": "Mdiamond",
                "style": "filled",
                "fillcolor": "white",
            },
            "END_LOOP": {
                "shape": "Msquare",
                "style": "filled",
                "fillcolor": "white",
            },
            "MERGE": {
                "shape": "ellipse",
                "style": "filled",
                "fillcolor": "lightgray",
            },
            "END": {
                "shape": "ellipse",
                "style": "filled",
                "fillcolor": "lightgreen",
            },
        }

        # Choose style based on node type
        style = styles.get(node.type, {"shape": "box"})
        self.dot.node(node.id, node.label, **style)

        # Draw all the children nodes of current node
        for child in node.children:
            self.dot.edge(node.id, child.id)
            self.add_nodes_edges(child)

    def create_visual_graph(self, output_file: str):
        """Create a visual representation of the execution flow graph"""
        self.dot.attr(rankdir="TB")

        if self.call_tracer.entry_node is None:
            raise ValueError(
                "No Entry Node found which infers no 'main' function present in file"
            )

        self.add_nodes_edges(self.call_tracer.entry_node)
        self.dot.render(output_file, view=True, format="png")
