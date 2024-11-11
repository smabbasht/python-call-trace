# very_complex_sample.py
import itertools
import random


def generate_data_sets():
    """Generates a list of data sets with random values"""
    data_sets = []
    a = 5
    int(a)
    random.randint(1, 100)
    for _ in range(5):
        data_set = [random.randint(1, 100) for _ in range(random.randint(5, 10))]
        data_sets.append(data_set)
    return set(data_sets)


def analyze_data_set(data_set):
    """Analyzes a single data set for statistical insights"""
    if not data_set:
        return {"average": None, "max": None, "min": None}

    total = sum(data_set)
    average = total / len(data_set)
    return {
        "average": average,
        "max": max(data_set),
        "min": min(data_set),
    }


def compare_data_sets(data_sets):
    """Compares all generated data sets to find similarities"""
    comparisons = {}
    for idx, (set1, set2) in enumerate(itertools.combinations(data_sets, 2)):
        common_elements = set(set1).intersection(set2)
        comparisons[f"comparison_{idx}"] = len(common_elements)
    return comparisons


def main():
    data_sets = generate_data_sets()
    all_statistics = [analyze_data_set(data_set) for data_set in data_sets]

    # Print statistics for each data set
    for idx, stats in enumerate(all_statistics):
        print(
            f"Data Set {idx + 1} Stats: Average: {stats['average']}, Max: {stats['max']}, Min: {stats['min']}"
        )

    # Sort data sets based on their average value
    sorted_data_sets = sorted(
        data_sets, key=lambda ds: sum(ds) / len(ds) if ds else 0, reverse=True
    )
    print("Data sets sorted by average value:", sorted_data_sets)

    # Compare data sets and print similarities
    comparisons = compare_data_sets(data_sets)
    for key, value in comparisons.items():
        print(f"{key}: {value} common elements")


if __name__ == "__main__":
    main()
