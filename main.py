# from flow_analyzer import ExecutionFlowAnalyzer
from flow_analyzer import ExecutionFlowAnalyzer
from graphing import GraphBuilder


def main():
    input_file = "input/test1.py"
    # input_file = "input/sample_program_enhanced.py"
    output_file = "output/execution_flow_graph.png"

    analyzer = ExecutionFlowAnalyzer()

    analyzer.analyze_file(input_file)
    print(analyzer)

    graph = GraphBuilder("Execution Flow Graph", analyzer)
    graph.create_visual_graph(output_file)

    print(f"Execution flow graph has been generated as '{output_file}'")


if __name__ == "__main__":
    main()
