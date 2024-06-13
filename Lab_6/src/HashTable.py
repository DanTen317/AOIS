from typing import List

import coverage

from Hash import Hash


class HashTable(object):
    def __init__(self):
        self.table: List[Hash] = []

    @staticmethod
    def __table_keys(table: List[Hash]) -> List[str]:
        table_keys = [item.keyword for item in table]
        return table_keys

    def __table_keys_values(self, table: List[Hash]) -> List[int]:
        table_keys_values = [item.keyword_value for item in table]
        return table_keys_values

    def add(self, key, value=""):
        try:
            if key in self.__table_keys(self.table):
                raise KeyError("Key already exists!")
            new_hash = Hash(key, value)
            self.table.append(self.step_by_step(new_hash))
            return True
        except KeyError as e:
            print("Exception:", e)
            return False
        except ValueError as e:
            print("Exception:", e)
            return False

    def update(self, key, value):  # todo
        if key in self.__table_keys(self.table):
            self.table[self.find(key)].value = value
        else:
            return False
        return True

    def delete(self, key):
        for item in self.table:
            deleted = item
            if item.keyword == key:
                self.table.remove(item)
                self.move_items()
                return True
        return False

    def step_by_step(self, new_hash: Hash):
        added: bool = False
        while not added:
            if new_hash.keyword_value not in self.__table_keys_values(self.table):
                added = True
            else:
                new_hash.keyword_value += 1
        return new_hash

    def move_items(self):
        list_of_used_hashes = []
        for item in self.table:
            # self.table[self.table.index(item)] = self.step_by_step(item)
            if item.keyword_value != Hash(item.keyword).keyword_value and item.keyword_value not in list_of_used_hashes:
                list_of_used_hashes.append(item.keyword_value)
                hash_to_move = Hash(item.keyword)
                while True:
                    if hash_to_move.keyword_value not in self.__table_keys_values(self.table):
                        self.table[self.table.index(item)] = hash_to_move
                        break
                    else:
                        hash_to_move.keyword_value += 1

    def find(self, key):
        expected = Hash(key)
        k_values = self.__table_keys_values(self.table)
        for i in range(len(k_values)):
            if key == self.table[i].keyword:
                return i


def main():
    table = HashTable()
    while (True):
        print("Hash Table:")
        for i in table.table:
            print(str(i))
        print("-"*10)
        option = input("  + to add\n  - to remove\n  = to update value\n  q to quit\n")
        if option == "q":
            break
        elif option == "+":
            if table.add(input("Key:"), input("Value:")):
                print("Successfully added")
            else:
                print("Failed to add")
        elif option == "-":
            if table.delete(input("Key:")):
                print("Successfully deleted")
            else:
                print("Failed to delete")
        elif option == "=":
            if table.update(input("Key:"), input("Value:")):
                print("Successfully updated")
            else:
                print("Failed to update")


if __name__ == '__main__':
    main()
