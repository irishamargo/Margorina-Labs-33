import random

def gen_random(num_count, begin, end):
    for _ in range(num_count):
        yield random.randint(begin, end)

if __name__ == "__main__":
    print("Test gen_random:")
    print("5 чисел от 1 до 3:")
    for num in gen_random(5, 1, 3):
        print(num, end=" ")
    print()

    print("\n10 чисел от 10 до 20:")
    for num in gen_random(10, 10, 20):
        print(num, end=" ")
    print()
