import numpy as np
import matplotlib.pyplot as plt
import time


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class OpenAddressingHashTable:
    def __init__(self):
        self.capacity = 19
        self.size = 0
        self.hash_table = [None for _ in range(self.capacity)]
        self.border = 0.5
        self.expansion = 0.75

    def __hash_func(self, key):
        x = 257
        str_sum = sum([ord(element) * x ** k for k, element in enumerate(key)])
        return str_sum % self.capacity

    def __second_hash_func(self, key):
        x = 257
        p = 100_000_007
        str_sum = sum([ord(element) * x ** k % p for k, element in enumerate(key)])
        return str_sum % p % self.capacity

    def __rehash_func(self, h, i, key):

        # linear probing
        # k = 1
        # rh = (h + i*k) % self.capacity

        # quadratic probing
        # c_1 = 0
        # c_2 = 1
        # rh = (h + c_1*i + c_2*(i**2)) % self.capacity

        # double hashing probing
        # need key in input parameters
        rh = (h + i * self.__second_hash_func(key)) % self.capacity

        return rh

    def add(self, key, value):
        h = self.__hash_func(key)
        probe_number = 1
        cell = Node(key, value)

        if self.hash_table[h] is None:
            self.hash_table[h] = cell
            self.size += 1
        else:
            if self.hash_table[h].key == key:
                self.hash_table[h].value = value
            else:
                next_h = self.__rehash_func(h, probe_number, key)
                while self.hash_table[next_h] and self.hash_table[next_h].key != key:
                    probe_number += 1
                    next_h = self.__rehash_func(next_h, probe_number, key)

                if self.hash_table[next_h] is None:
                    self.hash_table[next_h] = cell
                    self.size += 1
                else:
                    self.hash_table[next_h].value = value

        if self.size >= self.capacity * self.border:
            self.__expand()

    def find(self, key):
        start_h = self.__hash_func(key)
        probe_number = 1
        result = "Not found"
        cur_h = start_h

        if not self.hash_table[cur_h]:
            print(result)
            return result

        while self.hash_table[cur_h]:
            if self.hash_table[cur_h].key == key:
                result = self.hash_table[cur_h].value
                break
            cur_h = self.__rehash_func(cur_h, probe_number, key)
            probe_number += 1
            if cur_h == start_h:
                break

        print(result)
        return result

    def delete(self, key):
        start_h = self.__hash_func(key)
        probe_number = 1
        result = "Can't delete element: key not found"
        cur_h = start_h

        while self.hash_table[cur_h] is None:
            cur_h = self.__rehash_func(cur_h, probe_number, key)
            probe_number += 1
            if cur_h == start_h:
                print(result)
                return result

        if self.hash_table[cur_h].key == key:
            self.size -= 1
            result = self.hash_table[cur_h].value
            self.hash_table[cur_h] = None

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
            if cur_cell:
                # print(f"Computing hash for {cur_cell.key}: {cur_cell.value}")
                self.add(cur_cell.key, cur_cell.value)


def main():
    odht = OpenAddressingHashTable()

    # need generate data for best/mean/worst case
    inp_dict = {
        "'": "23",
        ":": "14",
        "M": "3",
        "`": "900",
        "s": "12",
    }

    standard_x = np.array([5e-5, 10e-5, 15e-5, 20e-5, 25e-5])
    x = []

    for key, value in inp_dict.items():
        # start_time = time.time()
        odht.add(key, value)
        # x.append(time.time() - start_time)

    for key in inp_dict.keys():
        # start_time = time.time()
        odht.find(key)
        # x.append(time.time() - start_time)

    for key in inp_dict.keys():
        start_time = time.time()
        odht.delete(key)
        x.append(time.time() - start_time)

    x = np.array(x)
    print(x)
    plt.plot(x, 'r', standard_x, 'b')
    plt.ylabel("time")
    plt.xlabel("step")
    plt.title("delete_double_worst")
    plt.show()

    # while True:
    #     inp_string = input().split()
    #     command = inp_string[0]
    #     number = inp_string[1]
    #     if command == 'add':
    #         if command == 'add':
    #             try:
    #                 name = inp_string[2]
    #                 odht.add(number, name)
    #             except IndexError:
    #                 print("You need to type value, try again!")
    #     else:
    #         if command == 'find':
    #             odht.find(number)
    #         elif command == 'del':
    #             odht.delete(number)
    #         else:
    #             print("Bad command!\nType this commands:\nadd, find, del")


main()