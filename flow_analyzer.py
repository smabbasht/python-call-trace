import ast
from typing import Optional, Dict, Set, List
from flow_node import FlowNode


class ExecutionFlowAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions: Dict[str, ast.FunctionDef] = {}
        self.current_node = None
        self.entry_node = None
        self.end_node = None
        self.visited_calls: Set[str] = set()
        self.test_visits: List[str] = list()

    def __str__(self):
        return f"Functions: {self.functions.keys()}, Visits: {self.test_visits}"

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

        if self.entry_node is None or self.end_node is None:
            raise ValueError("No entry or end node found")
        return self.entry_node, self.end_node

    def simulate_statement(self, stmt: ast.AST):
        """Simulate execution of a statement"""
        if isinstance(stmt, ast.If):
            self.simulate_if_statement(stmt)
        elif isinstance(stmt, ast.Expr):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)
            elif isinstance(stmt.value, (ast.ListComp, ast.GeneratorExp)):
                self.simulate_expression(stmt.value)
        elif isinstance(stmt, ast.For):
            self.simulate_for_loop(stmt)
        elif isinstance(stmt, ast.Assign):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)
            elif isinstance(stmt.value, (ast.ListComp, ast.GeneratorExp)):
                self.simulate_expression(stmt.value)
            else:
                self.simulate_expression(
                    stmt.value
                )  # Added to handle other expressions
        elif isinstance(stmt, ast.Return):
            if isinstance(
                stmt.value, (ast.Call, ast.ListComp, ast.GeneratorExp, ast.Dict)
            ):
                self.simulate_expression(stmt.value)
        elif isinstance(stmt, ast.Call):
            self.simulate_call(stmt)
        elif isinstance(stmt, ast.Attribute):
            self.simulate_attribute(stmt)
        elif isinstance(stmt, ast.Compare):
            for comparator in stmt.comparators:
                self.simulate_expression(comparator)
            self.simulate_expression(stmt.left)
        elif isinstance(stmt, ast.BinOp):
            self.simulate_expression(stmt.left)
            self.simulate_expression(stmt.right)
        elif isinstance(stmt, ast.UnaryOp):
            self.simulate_expression(stmt.operand)
        elif isinstance(stmt, ast.Lambda):  # Added to handle lambda expressions
            self.simulate_lambda(stmt)

    def simulate_call(self, node: ast.Call):
        """Simulate a function call and its arguments"""
        for arg in node.args:
            self.simulate_expression(arg)

        # Handle keyword arguments
        for keyword in node.keywords:
            self.simulate_expression(keyword.value)

        if isinstance(node.func, ast.Name):
            called_function = node.func.id
            self.simulate_function_call(called_function)
        elif isinstance(node.func, ast.Attribute):
            self.simulate_attribute(node.func)

    def simulate_attribute(self, node: ast.Attribute):
        """Simulate an attribute access"""
        self.simulate_expression(node.value)
        if isinstance(node.value, ast.Call):
            self.simulate_call(node.value)
        self.test_visits.append(node.attr)

    def simulate_expression(self, node: ast.AST):
        """Simulate an expression"""
        if isinstance(node, ast.Call):
            self.simulate_call(node)
        elif isinstance(node, ast.Attribute):
            self.simulate_attribute(node)
        elif isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            self.simulate_list_or_generator_expression(node)
        elif isinstance(node, ast.Dict):
            for key in node.keys:
                if key is not None:
                    self.simulate_expression(key)
            for value in node.values:
                self.simulate_expression(value)
        elif isinstance(node, ast.Lambda):
            self.simulate_lambda(node)
        elif isinstance(node, ast.BinOp):
            self.simulate_expression(node.left)
            self.simulate_expression(node.right)
        elif isinstance(node, ast.IfExp):
            self.simulate_expression(node.test)
            self.simulate_expression(node.body)
            self.simulate_expression(node.orelse)

    def simulate_lambda(self, node: ast.Lambda):
        """Simulate a lambda expression"""
        self.simulate_expression(node.body)

    def simulate_function_call(
        self, func_name: str, branch_point: Optional[FlowNode] = None
    ) -> FlowNode:
        """Simulate execution of a function, including all nested calls"""
        # Create a unique call signature to handle recursive calls
        call_signature = f"{func_name}_{id(branch_point)}"

        if func_name not in self.functions:
            # Handle built-in functions like print()
            call_node = self.create_node("FUNCTION", f"{func_name}")
            self.test_visits.append(func_name)
            if branch_point:
                branch_point.branch_merge_point = call_node
            return call_node

        # Create function node
        func_node = self.create_node("FUNCTION", f"{func_name}")

        # Process function body if we haven't seen this exact call before
        if call_signature not in self.visited_calls:
            self.visited_calls.add(call_signature)
            self.test_visits.append(func_name)

            func_def = self.functions[func_name]
            for stmt in func_def.body:
                self.simulate_statement(stmt)

            self.visited_calls.remove(call_signature)

        return func_node

    def simulate_if_statement(self, node: ast.If):
        """Simulate an if statement execution"""
        if isinstance(node.test, ast.Call):
            self.simulate_call(node.test)
        else:
            self.simulate_expression(node.test)  # Added to handle complex conditions

        prev_node = self.current_node

        # Process true branch
        for stmt in node.body:
            self.simulate_statement(stmt)
        true_end = self.current_node

        # Process false branch
        self.current_node = prev_node
        if node.orelse:
            for stmt in node.orelse:
                self.simulate_statement(stmt)

        # Create merge point if needed
        if true_end is not None:
            if true_end.branch_merge_point:
                self.current_node = true_end.branch_merge_point
            else:
                merge_node = self.create_node("MERGE", "Merge")
                if self.current_node != merge_node and self.current_node is not None:
                    self.current_node.add_child(merge_node)
                if true_end != merge_node:
                    true_end.add_child(merge_node)
                self.current_node = merge_node

    def simulate_for_loop(self, node: ast.For):
        """Simulate a for loop execution"""
        if isinstance(node.iter, ast.Call):
            self.simulate_call(node.iter)
        elif isinstance(node.iter, (ast.ListComp, ast.GeneratorExp)):
            self.simulate_list_or_generator_expression(node.iter)
        else:
            self.simulate_expression(node.iter)  # Added to handle complex iterables

        for stmt in node.body:
            self.simulate_statement(stmt)

    def simulate_list_or_generator_expression(
        self, node: ast.ListComp | ast.GeneratorExp
    ):
        """Simulate a list comprehension or generator expression"""
        for generator in node.generators:
            if isinstance(generator.iter, ast.Call):
                self.simulate_call(generator.iter)
            else:
                self.simulate_expression(generator.iter)

            # Handle condition if present
            for if_expr in generator.ifs:
                self.simulate_expression(if_expr)

        self.simulate_expression(node.elt)
