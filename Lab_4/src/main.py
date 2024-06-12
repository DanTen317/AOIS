from minimisation.truth_table.logical_function import LogicalFunction
from minimisation.minimisation import split_str_formula, glue_formula_steps, make_solvable
from prettytable import PrettyTable


def main():
    print(get_table_of_truth())

    summaryP = LogicalFunction("abp")
    summaryP.to_rpn()
    summaryP.evaluate_rpn()
    summaryP.res_dict.pop("res")
    summaryP.res_dict["P"] = [0, 0, 0, 1, 0, 1, 1, 1]
    print("SKNF P: ", summaryP.sknf())

    summaryS = LogicalFunction("abp")
    summaryS.to_rpn()
    summaryS.evaluate_rpn()
    summaryS.res_dict.pop("res")
    summaryS.res_dict["S"] = [0, 1, 1, 0, 1, 0, 0, 1]
    print("SKNF S: ", summaryS.sknf())

    to_minimiseP = split_str_formula(summaryP.sknf())
    to_minimiseS = split_str_formula(summaryS.sknf())

    minimisedP = make_solvable(glue_formula_steps(to_minimiseP, False), "|")
    minimisedS = make_solvable(glue_formula_steps(to_minimiseS, False), "|")
    print("SKNF P minimised: ", minimisedP)
    print("SKNF S minimised: ", minimisedS)

    s = LogicalFunction("abcd")
    s.to_rpn()
    s.evaluate_rpn()
    s.res_dict.pop("res")
    s.res_dict["y0"] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    print("Y0: ", s.sknf())
    print("Y0 min: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))

    s.res_dict["y1"] = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    print("Y1: ", s.sknf())
    print("Y1 min: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))

    s.res_dict["y2"] = [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
    print("Y2: ", s.sknf())
    print("Y2 min: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))

    s.res_dict["y3"] = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    print("Y3: ", s.sknf())
    print("Y3 min: ", make_solvable(glue_formula_steps(split_str_formula(s.sknf()), False), "|"))

    tt = PrettyTable()
    for key, value in s.res_dict.items():
        tt.add_column(key, value)
    print(tt)


def get_table_of_truth():
    lf = LogicalFunction("abp")
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
