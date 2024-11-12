from python_call_trace import PythonCallTrace
from graphing import GraphBuilder


def main():
    for i in range(1, 7):
        # input_file = str(input("Enter the file path: ")).strip()
        input_file = f"input/test_{i}.py"
        filename = input_file.split("/")[-1].split(".")[0]
        output_file = f"output/{filename}"

        analyzer = PythonCallTrace()

        analyzer.analyze_file(input_file)
        print(analyzer)

        graph = GraphBuilder(f"{filename} - Execution Flow Graph", analyzer)
        graph.create_visual_graph(output_file)

        print(f"Execution flow graph has been generated as '{output_file}.png'")


if __name__ == "__main__":
    main()
