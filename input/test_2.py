from itertools import combinations


def filter_and_apply(data, threshold):
    filtered_data = list(filter(lambda x: x > threshold, data))

    processed_data = [lambda x: x * 2 for _ in filtered_data]

    results = [func(value) for func, value in zip(processed_data, filtered_data)]

    print(f"Filtered data: {filtered_data}")
    print(f"Results after applying lambdas: {results}")


def analyze_combinations(data):
    for combo in combinations(data, 2):
        sum_combo = sum(combo)
        print(f"Combination: {combo}, Sum: {sum_combo}")


def main():
    data = [3, 5, 7, 2, 10, 1]
    filter_and_apply(data, 4)
    analyze_combinations(data)


if __name__ == "__main__":
    main()
