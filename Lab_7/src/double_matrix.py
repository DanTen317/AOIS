import random


class Operations:
    @staticmethod
    def disjunction(a, b):  # f7
        # print("Disjunction")
        c = ""
        for i in range(len(a)):
            if a[i] == "0" and b[i] == "0":
                c += "0"
            else:
                c += "1"
        return c

    @staticmethod
    def piers_operation(a, b):  # f8
        # print("Piers")
        c = ""
        for i in range(len(a)):
            if a[i] == "0" and b[i] == "0":
                c += "1"
            else:
                c += "0"
        return c

    @staticmethod
    def not_first(a, b):  # 2
        # print("Not First")
        c = ""
        for i in range(len(a)):
            if a[i] == "1" and b[i] == "0":
                c += "1"
            else:
                c += "0"
        return c

    @staticmethod
    def implication_from_first_to_second(a, b):  # 13
        # print("Implication from first to second")
        c = ""
        for i in range(len(a)):
            if a[i] == "1" and b[i] == "0":
                c += "0"
            else:
                c += "1"
        return c


class Matrix:
    def __init__(self, size=16):
        self.size = size
        self.matrix = [[0 for x in range(size)] for y in range(size)]
        self.randomise_matrix()

    def randomise_matrix(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = random.randint(0, 1)

    def read_word(self, index):
        try:
            word: str = "".join([str(self.matrix[i][index]) for i in range(len(self.matrix))])
            word = word[index:] + word[:index]
            return str(word)
        except IndexError:
            print("Index out of range")
            return False

    def get_address_column(self, index):
        try:
            address_column = ""
            _index = 0
            for i in range(index, len(self.matrix)):
                address_column += str(self.matrix[i][_index])
                _index += 1
            for i in range(0, index):
                address_column += str(self.matrix[i][_index])
                _index += 1
            return address_column
        except IndexError:
            print("Index out of range")
            return False

    def summarize_a_b(self, v_key="111"):
        try:
            if len(v_key) != 3:
                raise ValueError("Key must be 3 characters!")
            for it in v_key:
                if it not in "01":
                    raise ValueError("Key is wrong!")
            words = []
            for i in range(len(self.matrix)):
                words.append(self.read_word(i))
            words_to_summarize = []
            words_to_sum_dict = {}
            i = 0
            for it in words:
                if it[:3] == v_key:
                    words_to_summarize.append(it)
                    words_to_sum_dict[it] = i
                i += 1
            # print(words_to_summarize)
            # print(words_to_sum_dict)

            for word in words_to_summarize:
                word_cpy = word
                a = word[3:7]
                b = word[7:11]
                # print(a, b)
                c = bin(int(a, 2) + int(b, 2))[2:]
                if len(c) < 5:
                    c = "0" * (5 - len(c)) + c
                # print(c)

                word = v_key + a + b + c
                j = 0
                for i in range(words_to_sum_dict.get(word_cpy), len(self.matrix)):
                    self.matrix[i][words_to_sum_dict[word_cpy]] = int(word[j])
                    j += 1
                for i in range(words_to_sum_dict.get(word_cpy)):
                    self.matrix[i][words_to_sum_dict[word_cpy]] = int(word[j])
                    j += 1
                # print(word)
        except ValueError as e:
            print("Exception:", e)
            return False

    def _replace_word(self, index, value):
        words_dict = {}
        for i in range(len(self.matrix)):
            words_dict[self.read_word(i)] = i
        j = 0
        for i in range(index, len(self.matrix)):
            self.matrix[i][index] = int(value[j])
            j += 1
        for i in range(index):
            self.matrix[i][index] = int(value[j])
            j += 1

    def operations(self, index_first: int, index_second: int, index_result: int = None, operation: str = None):
        try:
            operation = operation.upper()
            first = self.read_word(index_first)
            second = self.read_word(index_second)
            result: str = ""
            if operation == "OR":
                result = Operations.disjunction(first, second)
            elif operation == "OR-NOT":
                result = Operations.piers_operation(first, second)
            elif operation == "NO F":
                result = Operations.not_first(first, second)
            elif operation == "NOT-NO FS":
                result = Operations.implication_from_first_to_second(first, second)
            else:
                return False

            if index_result is None:
                print(operation + ":", result)
            else:
                self._replace_word(index_result, result)
        except IndexError:
            print("Index out of range")

    def find_words_from_interval(self, from_str: str, to_str: str):
        words = []
        found = []
        from_int = int(from_str, 2)
        to_int = int(to_str, 2)
        for i in range(len(self.matrix)):
            words.append(self.read_word(i))
        for word in words:
            if from_int <= int(word, 2) <= to_int:
                found.append(word)
        return found
