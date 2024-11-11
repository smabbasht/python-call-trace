from flow_analyzer import ExecutionFlowAnalyzer


def test_file_1():
    input_file = "input/test_1.py"

    truth = "Functions: dict_keys(['validate_data', 'process_item', 'special_processing', 'normal_processing', 'main']), Visits: ['main', 'sort', 'process_item', 'validate_data', 'randint', 'print', 'print', 'print', 'print', 'special_processing', 'print', 'print', 'normal_processing', 'print', 'print']"

    analyzer = ExecutionFlowAnalyzer()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_2():
    input_file = "input/test_2.py"

    truth = "Functions: dict_keys(['filter_and_apply', 'analyze_combinations', 'main']), Visits: ['main', 'filter_and_apply', 'lambda', 'filter', 'list', 'lambda', 'zip', 'func', 'print', 'print', 'analyze_combinations', 'combinations', 'sum', 'print']"

    analyzer = ExecutionFlowAnalyzer()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_3():
    input_file = "input/test_3.py"

    truth = "Functions: dict_keys(['generate_data_sets', 'analyze_data_set', 'compare_data_sets', 'main']), Visits: ['main', 'generate_data_sets', 'int', 'randint', 'range', 'randint', 'range', 'randint', 'append', 'set', 'analyze_data_set', 'sum', 'len', 'max', 'min', 'enumerate', 'print', 'lambda', 'sum', 'len', 'sorted', 'print', 'compare_data_sets', 'combinations', 'enumerate', 'set', 'set', 'intersection', 'len', 'items', 'print']"

    analyzer = ExecutionFlowAnalyzer()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_4():
    input_file = "input/test_4.py"

    truth = "Functions: dict_keys(['process_numbers', 'conditional_analysis', 'nested_loop_example', 'main']), Visits: ['main', 'process_numbers', 'lambda', 'zip', 'op', 'print', 'conditional_analysis', 'print', 'print', 'print', 'print', 'print', 'nested_loop_example', 'len', 'range', 'len', 'range', 'print', 'print']"

    analyzer = ExecutionFlowAnalyzer()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth


def test_file_5():
    input_file = "input/test_5.py"

    truth = "Functions: dict_keys(['analyze_values', 'check_environment', 'conditional_operations', 'main']), Visits: ['main', 'analyze_values', 'abs', 'sqrt', 'max', 'min', 'print', 'print', 'check_environment', 'getenv', 'print', 'print', 'print', 'conditional_operations', 'round', 'print', 'pow', 'print', 'print']"

    analyzer = ExecutionFlowAnalyzer()
    analyzer.analyze_file(input_file)

    assert str(analyzer) == truth
