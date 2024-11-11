class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        return f"{self.name} barks"


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def speak(self):
        return f"{self.name} meows"


def animal_conversation(animal1, animal2):
    print(animal1.speak())
    print(animal2.speak())


def main():
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers", "Black")
    animal_conversation(dog, cat)


if __name__ == "__main__":
    main()
