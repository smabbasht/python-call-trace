import math
import os


def analyze_values(values):
    processed_values = [math.sqrt(abs(v)) for v in values if v > 0]
    max_value = max(processed_values) if processed_values else None
    min_value = min(processed_values) if processed_values else None
    print(f"Processed values: {processed_values}")
    print(f"Max value: {max_value}, Min value: {min_value}")


def check_environment():
    path = os.getenv("PATH", "Not Found")
    print(f"Environment PATH: {path}")

    if "usr" in path:
        print("Standard user directories found in PATH")
    else:
        print("User directories not found in PATH")


def conditional_operations(x):
    if x > 1000:
        print(f"Large number: {round(x, -2)}")
    elif x > 100:
        print(f"Medium number: {pow(x, 2)}")
    else:
        print(f"Small number: {x}")


def main():
    values = [16, -9, 25, -4, 36, 0]
    analyze_values(values)
    check_environment()
    conditional_operations(150)


if __name__ == "__main__":
    main()
