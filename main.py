from python_call_trace import PythonCallTrace
from graphing import GraphBuilder


def main():
    # Input and Output handling
    input_file = str(input("Please give path to source file: ")).strip()
    filename = input_file.split("/")[-1].split(".")[0]
    output_file = f"output/{filename}"

    # our Python Call Tracer
    tracer = PythonCallTrace()
    tracer.analyze_file(input_file)

    # Build Graph based on tracer's state
    graph = GraphBuilder(f"{filename} - Execution Flow Graph", tracer)
    graph.create_visual_graph(output_file)

    print(f"Execution flow graph has been generated as '{output_file}.png'")


if __name__ == "__main__":
    main()
