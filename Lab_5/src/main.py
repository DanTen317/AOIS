from minimisation.truth_table.logical_function import LogicalFunction
from minimisation.minimisation import split_str_formula, glue_formula_steps, make_solvable
from prettytable import PrettyTable


def main():
    # print(get_table_of_truth())

    # summaryP = LogicalFunction("abcv")
    # summaryP.to_rpn()
    # summaryP.evaluate_rpn()
    # summaryP.res_dict.pop("res")
    # # summaryP.res_dict["C"] = [0, 0, 0, 1, 0, 1, 1, 1]
    # print("SKNF P: ", summaryP.sknf())
    #
    # summaryS = LogicalFunction("abcv")
    # summaryS.to_rpn()
    # summaryS.evaluate_rpn()
    # summaryS.res_dict.pop("res")
    # # summaryS.res_dict["S"] = [0, 1, 1, 0, 1, 0, 0, 1]
    # print("SKNF S: ", summaryS.sknf())
    #
    # to_minimiseP = split_str_formula(summaryP.sknf())
    # to_minimiseS = split_str_formula(summaryS.sknf())
    #
    # minimisedP = make_solvable(glue_formula_steps(to_minimiseP, False), "|")
    # minimisedS = make_solvable(glue_formula_steps(to_minimiseS, False), "|")
    # print("SKNF P minimised: ", minimisedP)
    # print("SKNF S minimised: ", minimisedS)

    s = LogicalFunction("abcv")
    s.to_rpn()
    s.evaluate_rpn()
    s.res_dict.pop("res")

    a = list(s.res_dict.get("a"))
    a.insert(0, 1)
    a.pop()
    s.res_dict["a_"] = a

    b = list(s.res_dict.get("b"))
    b.pop()
    b.insert(0, 1)
    s.res_dict["b_"] = b

    c = list(s.res_dict.get("c"))
    c.pop()
    c.insert(0, 1)
    s.res_dict["c_"] = c

    y_a = []
    y_b = []
    y_c = []

    for i in range(0, len(a)):
        if s.res_dict.get("a")[i] != s.res_dict.get("a_")[i]:
            y_a.append(1)
        else:
            y_a.append(0)
    for i in range(0, len(b)):
        if s.res_dict.get("b")[i] != s.res_dict.get("b_")[i]:
            y_b.append(1)
        else:
            y_b.append(0)
    for i in range(0, len(c)):
        if s.res_dict.get("c")[i] != s.res_dict.get("c_")[i]:
            y_c.append(1)
        else:
            y_c.append(0)

    s.res_dict["y2"] = y_a
    print("Y2 sdnf: ", s.sdnf())
    print("Y2 min sdnf: ", make_solvable(glue_formula_steps(split_str_formula(s.sdnf()), False), "|"))
    print("Y2 sknf: ", s.sknf())
    print("Y2 min sknf: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))
    print()

    s.res_dict["y1"] = y_b
    print("Y1 sdnf: ", s.sdnf())
    print("Y1 min sdnf: ", make_solvable(glue_formula_steps(split_str_formula(s.sdnf()), False), "|"))
    print("Y1 sknf: ", s.sknf())
    print("Y1 min sknf: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))
    print()

    s.res_dict["y0"] = y_c
    print("Y0 sdnf: ", s.sdnf())
    print("Y0 min sdnf: ", make_solvable(glue_formula_steps(split_str_formula(s.sdnf()), False), "|"))
    print("Y0 sknf: ", s.sknf())
    print("Y0 min sknf: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))
    print()

    # s.res_dict["y3"] = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    # print("Y3: ", s.sknf())
    # print("Y3 min: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))

    tt = PrettyTable()
    for key, value in s.res_dict.items():
        tt.add_column(key, value)
    print(tt)


def get_table_of_truth():
    lf = LogicalFunction("abcv")
    lf.to_rpn()
    lf.evaluate_rpn()
    lf.res_dict.pop("res")
    lf.res_dict["S"] = [0, 1, 1, 0, 1, 0, 0, 1]
    lf.res_dict["P"] = [0, 0, 0, 1, 0, 1, 1, 1]
    table_of_truth = PrettyTable()
    for key, value in lf.res_dict.items():
        table_of_truth.add_column(key, value)
    return table_of_truth


if __name__ == '__main__':
    main()
