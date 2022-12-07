import numpy as np
import matplotlib.pyplot as plt
import time
import random
import string


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class ChainingHashTable:
    def __init__(self):
        self.capacity = 19
        self.size = 0
        self.hash_table = [None for _ in range(self.capacity)]
        self.x = 343
        self.counted_x = [self.x ** k for k in range(8)]
        self.border = 0.5
        self.expansion = 0.75

    def __hash_func(self, key):
        # classical polynomial hash function
        # x = 257
        # str_sum = sum([ord(element) * x ** k for k, element in enumerate(key)])

        # improved polynomial hash function
        # with using counted x
        # which increases speed by 64%
        if len(key) > len(self.counted_x):
            k = len(self.counted_x)
            degrees_to_add = len(key) - len(self.counted_x)
            for i in range(degrees_to_add):
                self.counted_x.append(self.x ** (k + i))

        str_sum = sum([ord(element) * self.counted_x[i] for i, element in enumerate(key)])
        return str_sum % self.capacity

    def add(self, key, value):
        h = self.__hash_func(key)
        cell = self.hash_table[h]
        node = Node(key, value)

        if not cell:
            self.hash_table[h] = node
            self.size += 1
        else:
            if self.hash_table[h].key == key:
                self.hash_table[h].value = value
            else:
                node.next = cell
                self.hash_table[h] = node
                self.size += 1

        if self.size >= self.capacity * self.border:
            self.__expand()

    def find(self, key):
        result = "Not found"
        h = self.__hash_func(key)
        cell = self.hash_table[h]

        if not cell:
            print(result)
            return result

        while cell:
            if cell.key == key:
                result = cell.value
                break
            cell = cell.next

        print(result)
        return result

    def delete(self, key):
        h = self.__hash_func(key)
        cell = self.hash_table[h]
        prev_cell = None

        while cell is not None and cell.key != key:
            prev_cell = cell
            cell = cell.next

        if cell is None:
            print("Can't delete element: key not found")
            return None
        else:
            self.size -= 1
            result = cell.value

            if prev_cell is None:
                self.hash_table[h] = None
            else:
                prev_cell.next = prev_cell.next.next

            print(result)
            return result

    def __expand(self):
        self.size = 0
        old_hash_table = self.hash_table
        old_capacity = self.capacity
        self.capacity = self.capacity + int(self.capacity * self.expansion)

        self.hash_table = [None for _ in range(self.capacity)]

        for i in range(old_capacity):
            cur_cell = old_hash_table[i]
            while cur_cell:
                # print(f"Computing hash for {cur_cell.key}: {cur_cell.value}")
                self.add(cur_cell.key, cur_cell.value)
                cur_cell = cur_cell.next


def main():
    cht = ChainingHashTable()

    # need generate data for best/mean/worst case
    # inp_dict = {
    #     "'": "23",
    #     ":": "14",
    #     "M": "3",
    #     "`": "900",
    #     "s": "12",
    # }
    #
    # standard_x = np.array([5e-5, 10e-5, 15e-5, 20e-5, 25e-5])
    # x = []

    # stress test
    inp_dict = {}
    letters = string.ascii_lowercase
    keys = [''.join(random.choice(letters) for _ in range(12)) for _ in range(100000)]
    values = [i+1 for i in range(100000)]

    for i in range(len(values)):
        inp_dict[keys[i]] = values[i]

    std_x = [1 for i in range(100000)]
    standard_x = np.array(std_x)
    x = []

    for key, value in inp_dict.items():
        start_time = time.time()
        cht.add(key, value)
        x.append(time.time() - start_time)

    for key in inp_dict.keys():
        # start_time = time.time()
        cht.find(key)
        # x.append(time.time() - start_time)

    for key in inp_dict.keys():
        # start_time = time.time()
        cht.delete(key)
        # x.append(time.time() - start_time)

    x = np.array(x)
    print(x)
    plt.plot(x, 'r', standard_x, 'b')
    plt.ylabel("time")
    plt.xlabel("step")
    plt.title("add")
    plt.show()

    # while True:
    #     inp_string = input().split()
    #     command = inp_string[0]
    #     number = inp_string[1]
    #     if command == 'add':
    #         try:
    #             name = inp_string[2]
    #             cht.add(number, name)
    #         except IndexError:
    #             print("You need to type value, try again!")
    #     else:
    #         if command == 'find':
    #             cht.find(number)
    #         elif command == 'del':
    #             cht.delete(number)
    #         else:
    #             print("Bad command!\nType this commands:\nadd, find, del")


main()
