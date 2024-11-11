def process_numbers(numbers):
    operations = [(lambda x: x**2 if x % 2 == 0 else x**3) for _ in numbers]

    results = [op(num) for op, num in zip(operations, numbers)]
    print(f"Processed results: {results}")


def conditional_analysis(value):
    if value > 100:
        print("Value is very large")
        if value % 2 == 0:
            print("Value is also even")
        else:
            print("Value is odd")
    elif value > 50:
        print("Value is moderately large")
    else:
        print("Value is small")


def nested_loop_example(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] % 2 == 0:
                print(f"Matrix[{i}][{j}] is even")
            else:
                print(f"Matrix[{i}][{j}] is odd")


def main():
    numbers = [3, 4, 7, 8, 10, 13]
    matrix = [[2, 5, 8], [11, 14, 17], [20, 23, 26]]

    process_numbers(numbers)
    conditional_analysis(75)
    nested_loop_example(matrix)


if __name__ == "__main__":
    main()
