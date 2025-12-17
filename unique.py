class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.items = iter(items)
        self.seen = set()

    def __next__(self):
        while True:
            try:
                item = next(self.items)
            except StopIteration:
                raise StopIteration

            if isinstance(item, str) and self.ignore_case:
                check_item = item.lower()
            else:
                check_item = item

            if check_item not in self.seen:
                self.seen.add(check_item)
                return item

    def __iter__(self):
        return self

if __name__ == "__main__":
    print("Test 1 - числа:")
    data = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    for item in Unique(data):
        print(item, end=" ")
    print()

    print("\nTest 2 - случайные числа:")
    from gen_random import gen_random
    data = gen_random(10, 1, 3)
    for item in Unique(data):
        print(item, end=" ")
    print()

    print("\nTest 3 - строки без ignore_case:")
    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    for item in Unique(data):
        print(item, end=" ")
    print()

    print("\nTest 4 - строки с ignore_case=True:")
    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    for item in Unique(data, ignore_case=True):
        print(item, end=" ")
    print()
