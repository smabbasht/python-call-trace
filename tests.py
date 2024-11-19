from python_call_trace import PythonCallTrace


def test_file_1():
    input_file = "input/test_1.py"

    i_th = int(input_file.split("/")[-1].split(".")[0].split("_")[-1])
    i_th = (i_th - 1) * 2
    truths = open("truths.txt", "r").readlines()
    truth = truths[i_th].strip() + "\n" + truths[i_th + 1].strip()

    analyzer = PythonCallTrace()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_2():
    input_file = "input/test_2.py"

    i_th = int(input_file.split("/")[-1].split(".")[0].split("_")[-1])
    i_th = (i_th - 1) * 2
    truths = open("truths.txt", "r").readlines()
    truth = truths[i_th].strip() + "\n" + truths[i_th + 1].strip()

    analyzer = PythonCallTrace()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_3():
    input_file = "input/test_3.py"

    i_th = int(input_file.split("/")[-1].split(".")[0].split("_")[-1])
    i_th = (i_th - 1) * 2
    truths = open("truths.txt", "r").readlines()
    truth = truths[i_th].strip() + "\n" + truths[i_th + 1].strip()

    analyzer = PythonCallTrace()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_4():
    input_file = "input/test_4.py"

    i_th = int(input_file.split("/")[-1].split(".")[0].split("_")[-1])
    i_th = (i_th - 1) * 2
    truths = open("truths.txt", "r").readlines()
    truth = truths[i_th].strip() + "\n" + truths[i_th + 1].strip()

    analyzer = PythonCallTrace()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_5():
    input_file = "input/test_5.py"

    i_th = int(input_file.split("/")[-1].split(".")[0].split("_")[-1])
    i_th = (i_th - 1) * 2
    truths = open("truths.txt", "r").readlines()
    truth = truths[i_th].strip() + "\n" + truths[i_th + 1].strip()

    analyzer = PythonCallTrace()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_6():
    input_file = "input/test_6.py"

    i_th = int(input_file.split("/")[-1].split(".")[0].split("_")[-1])
    i_th = (i_th - 1) * 2
    truths = open("truths.txt", "r").readlines()
    truth = truths[i_th].strip() + "\n" + truths[i_th + 1].strip()

    analyzer = PythonCallTrace()
    analyzer.analyze_file(input_file)

    print(analyzer)
    print(truth)

    assert str(analyzer) == truth


