import ast
from typing import Optional, Dict, Set
from flow_node import FlowNode


class ExecutionFlowAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions: Dict[str, ast.FunctionDef] = {}
        self.current_node = None
        self.entry_node = None
        self.end_node = None
        self.visited_calls: Set[str] = set()

    def create_node(
        self, node_type: str, label: str, ast_node: Optional[ast.AST] = None
    ) -> FlowNode:
        node = FlowNode(node_type, label, ast_node)
        if self.current_node:
            self.current_node.add_child(node)
        self.current_node = node
        return node

    def analyze_file(self, file_path: str) -> tuple[FlowNode, FlowNode]:
        """First pass: collect all function definitions"""
        with open(file_path, "r") as file:
            tree = ast.parse(file.read())

        # First pass: collect all function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.functions[node.name] = node

        # Start execution from main
        if "main" in self.functions:
            self.entry_node = self.create_node("ENTRY", "Program Start")
            self.simulate_function_call("main")

            # Add END node
            self.end_node = self.create_node("END", "Program Exit")
            if self.current_node:
                self.current_node.add_child(self.end_node)

        if self.entry_node is None or self.end_node is None:
            raise ValueError("No entry or end node found")
        return self.entry_node, self.end_node

    def analyze_code(self, code: str) -> tuple[FlowNode, FlowNode]:
        """Analyze code directly from string instead of file"""
        tree = ast.parse(code)

        # Collect all function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.functions[node.name] = node

        # Start execution from main
        if "main" in self.functions:
            self.entry_node = self.create_node("ENTRY", "Program Start")
            self.simulate_function_call("main")

            # Add END node
            self.end_node = self.create_node("END", "Program Exit")
            if self.current_node:
                self.current_node.add_child(self.end_node)

        if self.entry_node is None or self.end_node is None:
            raise ValueError("No entry or end node found")
        return self.entry_node, self.end_node

    def simulate_function_call(
        self, func_name: str, branch_point: Optional[FlowNode] = None
    ) -> FlowNode:
        """Simulate execution of a function, including all nested calls"""
        # Create a unique call signature to handle recursive calls
        call_signature = f"{func_name}_{id(branch_point)}"

        if func_name not in self.functions:
            # Handle built-in functions like print()
            call_node = self.create_node("CALL", f"Call: {func_name}")
            if branch_point:
                branch_point.branch_merge_point = call_node
            return call_node

        # Create function node
        func_node = self.create_node("FUNCTION", f"Function: {func_name}")
        # prev_node = self.current_node

        # Process function body if we haven't seen this exact call before
        if call_signature not in self.visited_calls:
            self.visited_calls.add(call_signature)

            func_def = self.functions[func_name]
            for stmt in func_def.body:
                self.simulate_statement(stmt, branch_point)

            self.visited_calls.remove(call_signature)

        return func_node

    def simulate_statement(
        self, stmt: ast.AST, branch_point: Optional[FlowNode] = None
    ):
        """Simulate execution of a statement"""
        if isinstance(stmt, ast.If):
            self.simulate_if_statement(stmt)
        elif isinstance(stmt, ast.Expr):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)
        elif isinstance(stmt, ast.For):
            self.simulate_for_loop(stmt)
        elif isinstance(stmt, ast.Assign):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)
        elif isinstance(stmt, ast.Return):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)

    def simulate_if_statement(self, node: ast.If):
        """Simulate an if statement execution"""
        if isinstance(node.test, ast.Call):
            self.simulate_call(node.test)

        # cond_node = self.create_node("CONDITION", f"IF: {ast.unparse(node.test)}")
        prev_node = self.current_node

        # Process true branch
        true_start = self.current_node
        for stmt in node.body:
            self.simulate_statement(stmt, true_start)
        true_end = self.current_node

        # Process false branch
        self.current_node = prev_node
        if node.orelse:
            for stmt in node.orelse:
                self.simulate_statement(stmt, true_start)

        # Create merge point if needed
        if true_end.branch_merge_point:
            self.current_node = true_end.branch_merge_point
        else:
            merge_node = self.create_node("MERGE", "Merge")
            if self.current_node != merge_node:
                self.current_node.add_child(merge_node)
            if true_end != merge_node:
                true_end.add_child(merge_node)
            self.current_node = merge_node

    def simulate_call(self, node: ast.Call):
        """Simulate a function call and its arguments"""
        for arg in node.args:
            if isinstance(arg, ast.Call):
                self.simulate_call(arg)

        if isinstance(node.func, ast.Name):
            called_function = node.func.id
            self.simulate_function_call(called_function)
        elif isinstance(node.func, ast.Attribute):
            pass

    def simulate_for_loop(self, node: ast.For):
        """Simulate a for loop execution"""
        if isinstance(node.iter, ast.Call):
            self.simulate_call(node.iter)

        for stmt in node.body:
            self.simulate_statement(stmt)
