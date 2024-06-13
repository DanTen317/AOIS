import re
from typing import List
from prettytable import PrettyTable


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