import ast
from typing import Optional, Dict, Set, List
from flow_node import FlowNode

class PythonCallTrace(ast.NodeVisitor):
    def __init__(self):
        self.function_defs: Dict[str, ast.FunctionDef] = {}  # Track function definitions
        self.class_defs: Dict[str, ast.ClassDef] = {}  # Track class definitions
        self.current_node = None
        self.entry_node = None
        self.end_node = None
        self.visited_calls: Set[str] = set()  # Track pending function calls
        self.visit_log: List[str] = list()  # Persistent visit_log for testing
        self.in_super_call = False  # Track if we're inside a super() call

    def __str__(self):
        return f"Functions: {self.function_defs.keys()}\nVisits: {self.visit_log}"

    def create_node(self, node_type: str, label: str, ast_node: Optional[ast.AST] = None) -> FlowNode:
        """Create a new flow node"""
        node = FlowNode(node_type, label, ast_node)
        if self.current_node:
            self.current_node.add_child(node)
        self.current_node = node
        return node

    def analyze_file(self, file_path: str) -> tuple[FlowNode, FlowNode]:
        """Analyze the given Python file to trace function and class definitions,
        and simulate the execution starting from the 'main' function."""
        with open(file_path, "r") as file:
            tree = ast.parse(file.read())

        # First pass: collect all function and class definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.function_defs[node.name] = node
            elif isinstance(node, ast.ClassDef):
                self.class_defs[node.name] = node

        # Start execution from main
        if "main" in self.function_defs:
            self.entry_node = self.create_node("ENTRY", "Program Start")
            self.simulate_function_call("main")
            self.end_node = self.create_node("END", "Program Exit")

        if self.entry_node is None or self.end_node is None:
            raise ValueError("No entry or end node found")
        return self.entry_node, self.end_node

    def get_base_classes(self, class_name: str) -> List[str]:
        """Get the base classes of a given class for super() calls"""
        if class_name in self.class_defs:
            class_def = self.class_defs[class_name]
            return [base.id for base in class_def.bases if isinstance(base, ast.Name)]
        return []

    def simulate_call(self, node: ast.Call):
        """Simulate a function call and its arguments"""
        # Check if this is a super() call
        is_super_call = (
            isinstance(node.func, ast.Name) and node.func.id == "super"
        ) or (
            isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "super"
        )

        # Skip logging super() calls
        if is_super_call:
            self.in_super_call = True
            return

        for arg in node.args:
            self.simulate_expression(arg)

        for keyword in node.keywords:
            self.simulate_expression(keyword.value)

        if isinstance(node.func, ast.Name):
            called_function = node.func.id
            if called_function in self.class_defs:
                # Handle class instantiation
                self.visit_log.append(called_function)

                # Get inheritance chain
                class_chain = []
                current_class = called_function
                while current_class:
                    class_chain.append(current_class)
                    bases = self.get_base_classes(current_class)
                    current_class = bases[0] if bases else None

                # Call constructors from base to derived
                for class_name in reversed(class_chain):
                    if f"{class_name}.__init__" not in self.visited_calls:
                        self.simulate_function_call(f"{class_name}.__init__")
            else:
                self.simulate_function_call(called_function)
        elif isinstance(node.func, ast.Attribute):
            if not self.in_super_call:  # Only process if not in a super() call
                self.simulate_attribute(node.func)

        self.in_super_call = False  # Reset super call flag

    def simulate_statement(self, stmt: ast.AST):
        """Simulate execution of a statement"""
        if isinstance(stmt, ast.If):
            self.simulate_if_statement(stmt)
        elif isinstance(stmt, ast.Expr):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)
            elif isinstance(stmt.value, (ast.ListComp, ast.GeneratorExp)):
                self.simulate_expression(stmt.value)
        elif isinstance(stmt, (ast.For, ast.While)):
            self.simulate_loop(stmt)
        elif isinstance(stmt, ast.Assign):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)
            elif isinstance(stmt.value, (ast.ListComp, ast.GeneratorExp)):
                self.simulate_expression(stmt.value)
            else:
                self.simulate_expression(stmt.value)
        elif isinstance(stmt, ast.Return):
            if isinstance(stmt.value, ast.Call):
                self.simulate_call(stmt.value)
            elif isinstance(stmt.value, (ast.JoinedStr, ast.FormattedValue)):
                self.simulate_expression(stmt.value)
        elif isinstance(stmt, ast.Call):
            self.simulate_call(stmt)

    def simulate_attribute(self, node: ast.Attribute):
        """Simulate an attribute access"""
        if not self.in_super_call:  # Skip if in super() call
            self.simulate_expression(node.value)
            if isinstance(node.value, ast.Call):
                self.simulate_call(node.value)
            self.visit_log.append(node.attr)

    def simulate_expression(self, node: ast.AST):
        """Simulate an expression"""
        if isinstance(node, ast.Call):
            self.simulate_call(node)
        elif isinstance(node, ast.Attribute):
            self.simulate_attribute(node)
        elif isinstance(node, (ast.JoinedStr, ast.FormattedValue)):
            if isinstance(node, ast.JoinedStr):
                for value in node.values:
                    self.simulate_expression(value)
            elif isinstance(node, ast.FormattedValue):
                self.simulate_expression(node.value)
        elif isinstance(node, ast.Name):
            pass  # Skip to avoid logging variable names

    def simulate_function_call(
        self, func_name: str, branch_point: Optional[FlowNode] = None
    ) -> FlowNode:
        """Simulate execution of a function, including all nested calls"""
        call_signature = f"{func_name}_{id(branch_point)}"

        if ( not func_name.endswith(".__init__") or call_signature not in self.visited_calls):
            self.visit_log.append(func_name)

        func_node = self.create_node("FUNCTION", f"{func_name}")

        if call_signature not in self.visited_calls:
            self.visited_calls.add(call_signature)

            pure_func_name = func_name.split(".")[-1]
            class_name = func_name.split(".")[0] if "." in func_name else None

            func_def = None
            if class_name and class_name in self.class_defs:
                for node in self.class_defs[class_name].body:
                    if (
                        isinstance(node, ast.FunctionDef)
                        and node.name == pure_func_name
                    ):
                        func_def = node
                        break
            else:
                func_def = self.function_defs.get(pure_func_name)

            if func_def:
                for stmt in func_def.body:
                    self.simulate_statement(stmt)

            self.visited_calls.remove(call_signature)

        return func_node

    def trim_text(self, text: str, n: int) -> str:
        """Trim text to a maximum of 20 characters."""
        if len(text) > n:
            return text[:n] + '...'
        return text

    def simulate_if_statement(self, node: ast.If):
        """Simulate an if statement as a branch with condition."""
        condition_text = self.trim_text(f"if {ast.unparse(node.test)}:", 15)
        condition_node = self.create_node('CONDITION', condition_text, node)

        # Process true branch
        for stmt in node.body:
            self.simulate_statement(stmt)
        end_true_branch = self.current_node

        # Reset to condition node for the false branch
        self.current_node = condition_node
        for stmt in node.orelse:
            self.simulate_statement(stmt)
        end_false_branch = self.current_node

        # Create a merge node that both branches connect to
        merge_node = self.create_node('END_IF', 'End Conditional', node)
        if end_true_branch:
            end_true_branch.add_child(merge_node)
        if end_false_branch:
            end_false_branch.add_child(merge_node)
        self.current_node = merge_node

    def simulate_loop(self, node: ast.For | ast.While):
        """Simulate a loop execution as a branch with cyclic paths."""
        # Create a loop entry node with loop condition as label
        if isinstance(node, ast.For):
            loop_text = self.trim_text(f"for {' '.join(ast.unparse(node.target).split())} in {' '.join(ast.unparse(node.iter).split())}:", 25)
        else:  # ast.While
            loop_text = self.trim_text(f"while {' '.join(ast.unparse(node.test).split())}:", 25)
        loop_entry = self.create_node('LOOP_START', loop_text, node)

        # Simulate the loop body
        for stmt in node.body:
            self.simulate_statement(stmt)

        if self.current_node:
            self.current_node.add_child(loop_entry)
            self.current_node = loop_entry

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
