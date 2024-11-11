# from flow_analyzer import ExecutionFlowAnalyzer
from flow_analyzer import ExecutionFlowAnalyzer
from graphing import GraphBuilder


def main():
    input_file = "input/test_5.py"
    output_file = f"output/{input_file.split('/')[-1].split('.')[0]}"

    analyzer = ExecutionFlowAnalyzer()

    analyzer.analyze_file(input_file)
    print(analyzer)

    graph = GraphBuilder("Execution Flow Graph", analyzer)
    graph.create_visual_graph(output_file)

    print(f"Execution flow graph has been generated as '{output_file}'")


if __name__ == "__main__":
    main()
