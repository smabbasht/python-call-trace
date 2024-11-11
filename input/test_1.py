from random import randint


def validate_data(value):
    a = randint(0, 100)
    print(a)
    if value > 0:
        print("Positive value")
        return True
    else:
        print("Non-positive value")
        return False


def process_item(item):
    if validate_data(item):
        if item > 100:
            print("Large value")
            special_processing()
        else:
            print("Normal value")
            normal_processing()
    else:
        print("Invalid item")


def special_processing():
    print("Performing special processing")


def normal_processing():
    print("Performing normal processing")


def main():
    items = [50, 150, -10]
    items.sort()
    for item in items:
        process_item(item)


if __name__ == "__main__":
    main()
