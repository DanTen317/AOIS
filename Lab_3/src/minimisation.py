import re
from typing import List
from prettytable import PrettyTable
from truth_table.logical_function import LogicalFunction


def split_str_formula(formula_str: str) -> List[List[str]]:
    formula = []
    if len(re.findall(r"\(.&", formula_str)) > 0:
        formula_str = formula_str.replace("&", "")
        formula = formula_str.split("|")
    elif len(re.findall(r"\(.|", formula_str)) > 0:
        formula_str = formula_str.replace("|", "")
        formula = formula_str.split("&")
    for i in range(len(formula)):
        item = formula[0]
        formula.remove(item)
        item = item.replace("(", "")
        item = item.replace(")", "")
        formula.append(item)
    formula_items: List[List[str]] = []
    for it in formula:
        it = [*it]
        formula_items.append(it)
    index = 0
    for it in formula_items:
        for i in range(len(it)):
            if it[i] == "!":
                it[i] = ""
                it[i + 1] = "!" + it[i + 1]
        it_cpy = []
        [it_cpy.append(x) for x in it if x != ""]
        formula_items[index] = it_cpy
        index += 1
    return formula_items


# formula = formula_str.split("")
def glue_formula(formula: List[List[str]]):
    glued_formula: List[List[str]] = []
    unused_items: List[List[str]] = []
    for item1 in formula:
        unused: bool = True
        for item2 in formula:
            has_common_element: bool = False
            item_to_add: List[str] = []
            num_of_eq_items: int = 0
            for it1 in item1:
                for it2 in item2:
                    if it1 == it2:
                        num_of_eq_items += 1
                        item_to_add.append(it1)
                    elif it1.replace("!", "") == it2.replace("!", ""):
                        has_common_element = True
            if num_of_eq_items == len(item1) - 1 and has_common_element:
                glued_formula.append(item_to_add)
                unused = False
        if unused:
            unused_items.append(item1)
    res = []
    [res.append(x) for x in glued_formula if x not in res]
    glued_formula = res
    glued_formula = glued_formula + unused_items
    return glued_formula


def glue_formula_steps(formula: List[List[str]], print_steps: bool = True):

    glued_formula: List[List[str]] = formula
    n = len(glued_formula[0])
    step = 1
    while n - 1 != 0:
        glued_formula = glue_formula(glued_formula)
        if print_steps:
            print("step ", step, ":")
            print(glued_formula)
        step += 1
        n -= 1
    return glued_formula


def make_solvable(formula: List[List[str]], operation: str):
    f: List[str] = []
    for i in range(len(formula)):
        f.append(operation.join(formula[i]))
    if operation == "&":
        return "(" + ")|(".join(f) + ")"
    elif operation == "|":
        return "(" + ")&(".join(f) + ")"


def build_table(form: str):
    formula = LogicalFunction(form)
    formula.to_rpn()
    truth_table = formula.evaluate_rpn()
    sdnf = formula.sdnf()
    sknf = formula.sknf()

    glued_sdnf = glue_formula_steps(split_str_formula(sdnf), False)
    glued_sknf = glue_formula_steps(split_str_formula(sknf), False)

    sdnf_table = gen_table(sdnf, glued_sdnf, "|")
    print("SDNF table:")
    print(sdnf_table)
    sknf_table = gen_table(sknf, glued_sknf, "&")
    print("SKNF table:")
    print(sknf_table)


def gen_table(full_formula: str, glued_formula, what_f: str) -> PrettyTable:
    output = PrettyTable()
    output.add_column("", [what_f.join(it) for it in glued_formula])

    for item in split_str_formula(full_formula):
        column = []
        for it in glued_formula:
            is_in: bool = False
            for i in it:
                if i in item:
                    is_in = True
                else:
                    is_in = False
                    break
            if is_in:
                column.append("x")
            else:
                column.append(" ")
        output.add_column(what_f.join(item), column)
    return output


def build_karnaugh(form: str):
    formula = LogicalFunction(form)
    formula.to_rpn()
    truth_table = formula.evaluate_rpn()

    rows: int = int(len(formula.variables) / 2)
    columns: int = int(len(formula.variables) - rows)
    row_values: List[str] = ["0" * rows for _ in range(2 ** rows)]
    col_values: List[str] = ["0" * columns for _ in range(2 ** columns)]

    row_vars: List[str] = [var for var in formula.variables[:rows]]
    col_vars: List[str] = [var for var in formula.variables[rows:]]

    col_values = get_gray_code(col_values)
    for i in range(len(row_values)):
        it = decimalToBinary(i)
        if len(it) < len(row_values[i]):
            it = "0" * (len(row_values[i]) - len(it)) + it
        row_values[i] = it

    output = PrettyTable()
    output.add_column(f"{"".join(row_vars)}\\{"".join(col_vars)}", row_values)

    # variables_dict = {it: [] for it in col_vars+row_vars}
    # for i in range(len(row_vars)):
    #     for j in range(len(row_values)):
    #         variables_dict.update({row_vars[i]: variables_dict.get(row_vars[i]) + [row_values[j][i]]})
    # for i in range(len(row_vars)):
    #     for j in range(len(row_values)):
    #         variables_dict.update({row_vars[i]: variables_dict.get(row_vars[i]) + [row_values[j][i]]})
    # print("---",variables_dict)
    #
    # for i in range(truth_table[-1]):
    #     to_add: bool = False
    #     for item in truth_table:
    #         for j in range(len(truth_table.get(item))):
    #             pass
    #     for item in formula.variables:
    #         if item == truth_table[item][i]:
    #             to_add = True
    #         else:
    #             to_add = False
    #             break
    #     if to_add:
    #         pass
    # print(truth_table.get("res"))
    a = truth_table["a"]
    b = truth_table["b"]
    c = truth_table["c"]

    for bc_value in col_values:
        column = []
        for a_value in row_values:
            a_indices = [i for i, el in enumerate(a) if el == int(a_value)]
            b_indices = [i for i, el in enumerate(b) if el == int(bc_value[0])]
            c_indices = [i for i, el in enumerate(c) if el == int(bc_value[1])]
            index = None
            for i in a_indices:
                if i in b_indices and i in c_indices:
                    index = i
                    break
            column.append(truth_table.get("res")[index])
        output.add_column(bc_value, column)
    print(output)
    print("glued SDNF:", make_solvable(glue_formula_steps(split_str_formula(sdnf), False), operation="|"))
    print("glued SKNF:", make_solvable(glue_formula_steps(split_str_formula(sknf), False), operation="&"))
    return output


def get_gray_code(values_list):
    for i in range(len(values_list)):
        if i < len(values_list) / 2:
            it: str = decimalToBinary(i)
        else:
            it: str = decimalToBinary(len(values_list) - 1 - i + int(len(values_list) / 2))
        if len(it) < len(values_list[i]):
            it = "0" * (len(values_list[i]) - len(it)) + it
        values_list[i] = it
    return values_list


def decimalToBinary(n):
    return bin(n).replace("0b", "")


formula = "(a&b)|!c"  # Start here

lf = LogicalFunction(formula)
lf.to_rpn()
lf.evaluate_rpn()
sdnf = lf.sdnf()
sknf = lf.sknf()

print("SDNF:", sdnf)
# print(split_str_formula(sdnf))
print("glued SDNF:", make_solvable(glue_formula_steps(split_str_formula(sdnf)), operation="|"))
print("SKNF:", sknf)
# print(split_str_formula(sknf))
print("glued SKNF:", make_solvable(glue_formula_steps(split_str_formula(sknf)), operation="&"))

print()
print("solve-table:")
build_table(formula)

print()
print("karnaugh table:")
build_karnaugh(formula)
