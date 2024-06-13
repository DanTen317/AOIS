from typing import List

from prettytable import PrettyTable

options = {
    '&': lambda x, y: x and y,
    '|': lambda x, y: x or y,
    '!': lambda x: not x,
    '->': lambda x, y: x <= y,
    '~': lambda x, y: x == y
}


def process_input(function_str):
    # Разрешенные символы
    allowed_symbols = "abcdv&|!->~()"

    # Проверка наличия недопустимых символов
    for char in function_str:
        if char not in allowed_symbols:
            return False

    # Проверка количества открывающих и закрывающих скобок
    open_brackets = function_str.count("(")
    close_brackets = function_str.count(")")
    if open_brackets != close_brackets:
        return False

    return True


class LogicalFunction:
    def __init__(self, function: str):
        self.rpn: str = ""
        # self.truth_table: dict = {}
        self.variables = []
        self._variables_values_list: dict[str:List[bool]] = {}
        self.operators = "&|!>~"
        self.precedence = {"&": 2, "|": 2, "!": 3, ">": 1, "~": 1}
        self.function: str = self.is_valid_function(function)
        self.variable_value_filler()
        self.res_dict: dict[str:List[int]] = {}

    def is_valid_function(self, function_str: str):
        function_str = function_str.lower()
        allowed_symbols = "abcdv&|!->~()"

        # Проверка наличия недопустимых символов
        for token in function_str:
            if token not in allowed_symbols:
                del self
                # self.__del__()

        # Проверка количества открывающих и закрывающих скобок
        open_brackets = function_str.count("(")
        close_brackets = function_str.count(")")
        if open_brackets != close_brackets:
            del self
            # self.__del__()

        function_str = function_str.replace("->", ">")
        for token in function_str:
            if token in "abcdv" and token not in self.variables:
                self.variables.append(token)
        self.variables.sort()
        return function_str

    def variable_value_filler(self):
        for item in self.variables:
            self._variables_values_list[item] = []

        bin_str = ""
        for i in range(0, len(self.variables)):
            bin_str += "0"
        bin_num = bin(0)
        self.variables.reverse()
        for i in range(0, 2 ** len(self.variables)):
            for j in range(0, len(self.variables)):
                self._variables_values_list[self.variables[j]].append(i >> j & 1)
            bin_num = bin_num + bin(1)
        self.variables.reverse()

    def to_rpn(self):
        stack = []
        rpn = []
        for token in self.function:
            if token in self.operators:
                while stack and stack[-1] in self.operators and self.precedence[stack[-1]] >= self.precedence[token]:
                    rpn.append(stack.pop())
                stack.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack[-1] != "(":
                    rpn.append(stack.pop())
                stack.pop()
            else:
                rpn.append(token)

        while stack:
            rpn.append(stack.pop())
        self.rpn = "".join(rpn)
        # print("".join(rpn))

    def evaluate_rpn(self):
        for variable in self.variables:
            self.res_dict[variable] = []
        self.res_dict["res"] = []
        for i in range(0, 2 ** len(self.variables)):
            rpn_str = self.rpn
            for item in self._variables_values_list.keys():
                rpn_str = rpn_str.replace(item, str(self._variables_values_list[item][i]))
                self.res_dict[item].append(self._variables_values_list[item][i])

            stack = []
            token_counter = 0
            operator_counter = 1

            for token in rpn_str:
                if token in self.operators:
                    if token == "!":
                        operand_2: bool = stack.pop()
                    else:
                        operand_2: bool = stack.pop()
                        operand_1: bool = stack.pop()

                    if token == "&":
                        result = operand_1 and operand_2
                        if f"& ({operator_counter})" not in self.res_dict.keys():
                            self.res_dict[f"& ({operator_counter})"] = [int(result == True)]
                        else:
                            self.res_dict[f"& ({operator_counter})"].append(int(result == True))
                    elif token == "|":
                        result = operand_1 or operand_2
                        if f"| ({operator_counter})" not in self.res_dict.keys():
                            self.res_dict[f"| ({operator_counter})"] = [int(result == True)]
                        else:
                            self.res_dict[f"| ({operator_counter})"].append(int(result == True))
                    elif token == "!":
                        # if token_counter != (len(rpn_str) - 1):
                        #     stack.append(operand_1)
                        result = not operand_2
                        if f"! ({operator_counter})" not in self.res_dict.keys():
                            self.res_dict[f"! ({operator_counter})"] = [int(result == True)]
                        else:
                            self.res_dict[f"! ({operator_counter})"].append(int(result == True))
                    elif token == ">":
                        result = not operand_1 or operand_2
                        if f"-> ({operator_counter})" not in self.res_dict.keys():
                            self.res_dict[f"-> ({operator_counter})"] = [int(result == True)]
                        else:
                            self.res_dict[f"-> ({operator_counter})"].append(int(result == True))
                    else:
                        result = operand_1 == operand_2
                        if f"~ ({operator_counter})" not in self.res_dict.keys():
                            self.res_dict[f"~ ({operator_counter})"] = [int(result == True)]
                        else:
                            self.res_dict[f"~ ({operator_counter})"].append(int(result == True))
                    stack.append(result)
                    operator_counter += 1
                else:
                    stack.append((token == "1") is True)
                token_counter += 1
            self.res_dict["res"].append(int(stack[0]))
            #     print(stack[0])
            # print(self._variables_values_list.items())
            # for item in self.res_dict.keys():
            #     print(item.title(), self.res_dict[item])
        # for each_row in zip(*([i] + (j)
        #         #                       for i, j in self.res_dict.items())):
        #         #     print(*each_row, " ")
        return self.res_dict

    def sdnf(self):
        sdnf: str = ""
        for item in range(0, 2 ** len(self.variables)):
            if self.res_dict[list(self.res_dict)[-1]][item] == 1:
                i: int = 0
                sdnf += "("
                for variable in list(self.res_dict.keys()):
                    if i >= len(self.variables):
                        break
                    if i != (len(self.variables) - 1):
                        if self.res_dict[variable][item] == 1:
                            sdnf += str(f"{variable}&")
                        else:
                            sdnf += str(f"!{variable}&")
                    else:
                        if self.res_dict[variable][item] == 1:
                            sdnf += str(f"{variable}")
                        else:
                            sdnf += str(f"!{variable}")
                    i += 1
                sdnf += ")|"
        sdnf = sdnf[:-1]
        return sdnf

    def num_sdnf(self):
        result: str = "("
        for item in range(0, 2 ** len(self.variables)):
            if self.res_dict[list(self.res_dict)[-1]][item] == 1:
                bin_num: str = ""
                i: int = 0
                for variable in list(self.res_dict.keys()):
                    if i < len(self.variables):
                        bin_num += str(self.res_dict[variable][item])
                        i += 1
                    else:
                        break
                num: int = int(bin_num, 2)
                result += str(num)
                result += ", "
        result = result[:-2]
        result += ") |"
        return result

    def sknf(self):
        sknf: str = ""
        for item in range(0, 2 ** len(self.variables)):
            if self.res_dict[list(self.res_dict)[-1]][item] == 0:
                i: int = 0
                sknf += "("
                for variable in list(self.res_dict.keys()):
                    if i >= len(self.variables):
                        break
                    if i != (len(self.variables) - 1):
                        if self.res_dict[variable][item] == 1:
                            sknf += str(f"!{variable}|")
                        else:
                            sknf += str(f"{variable}|")
                    else:
                        if self.res_dict[variable][item] == 1:
                            sknf += str(f"!{variable}")
                        else:
                            sknf += str(f"{variable}")
                    i += 1
                sknf += ")&"
        sknf = sknf[:-1]
        return sknf

    def num_sknf(self):
        result: str = "("
        for item in range(0, 2 ** len(self.variables)):
            if self.res_dict[list(self.res_dict)[-1]][item] == 0:
                bin_num: str = ""
                i: int = 0
                for variable in list(self.res_dict.keys()):
                    if i < len(self.variables):
                        bin_num += str(self.res_dict[variable][item])
                        i += 1
                    else:
                        break
                num: int = int(bin_num, 2)
                result += str(num)
                result += ", "
        result = result[:-2]
        result += ") &"
        return result

    def index_form(self):
        a = self.res_dict[list(self.res_dict)[-1]]
        for i in range(0, len(a)):
            a[i] = str(a[i])
        return "".join(a) + " - " + str(int("".join(a), 2))


def dict_to_table(dictionary):
    table = PrettyTable()
    for key, value in dictionary.items():
        table.add_column(key, value, "c")
    return table

# t = LogicalFunction("!((c|(!d))->b)")
# t.to_rpn()
# t.evaluate_rpn()
# print(t.sdnf())
# print(t.sknf())
# print(t.num_sdnf())
# print(t.num_sknf())
# print(t.index_form())


# def main():
#     while True:
#         while True:
#             formula = input("Enter formula (q - quit): ")
#             if formula == "q":
#                 break
#             if not (process_input(formula)):
#                 print("Invalid formula!")
#             else:
#                 break
#         if formula == "q":
#             break
#         func = LogicalFunction(formula)
#         func.to_rpn()
#         func.evaluate_rpn()
#         print(func.sdnf())
#         print(func.sknf())
#         print(func.num_sdnf())
#         print(func.num_sknf())
#         print(func.index_form())
#
#
# if __name__ == "__main__":
#     main()
