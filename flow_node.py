import ast
import uuid
from typing import Optional


class FlowNode:
    def __init__(self, node_type: str, label: str, ast_node: Optional[ast.AST] = None):
        self.id = str(uuid.uuid4())
        self.type = node_type
        self.label = label
        self.ast_node = ast_node
        self.children = []
        self.parents = []
        self.branch_merge_point = None

    def __str__(self):
        # Define Serializer for the class
        return f"{self.type} {self.label}"

    def add_child(self, child: "FlowNode"):
        # Check if it already exists in child's parents or self's children
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            child.parents.append(self)

    def set_branch_merge_point(self, node: "FlowNode"):
        # Initialize branch_merge_point
        self.branch_merge_point = node
