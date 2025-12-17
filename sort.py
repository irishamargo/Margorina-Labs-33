data = [5, -5, 3, -3, 10, -10, 1, -1, 0, 7, -7]

if __name__ == '__main__':
    result = sorted(data, key=abs, reverse=True)
    print("Без lambda:", result)

    result_with_lambda = sorted(data, key=lambda x: abs(x), reverse=True)
    print("С lambda:", result_with_lambda)
