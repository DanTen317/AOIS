import unittest

from minimisation import *
from truth_table.logical_function import LogicalFunction


class MyTestCase(unittest.TestCase):
    def test_karnaugh(self):
        formula = "(a&b)->c"
        f = build_karnaugh(formula)
        pt = PrettyTable()
        pt.add_column("a\\bc", ["0", "1"])
        pt.add_column("00", ["1", "1"])
        pt.add_column("01", ["1", "1"])
        pt.add_column("11", ["1", "0"])
        pt.add_column("10", ["1", "1"])
        self.assertEqual(f.rows[0],['0', 1, 1, 1, 1])
        self.assertEqual(f.rows[1],['1', 1, 1, 1, 0])

    def test_gen_table(self):
        full_formula: str = '(!a&!b&!c)|(!a&b&!c)|(a&!b&!c)|(a&b&!c)|(a&b&c)'
        glued_formula = [['!c'], ['a', 'b']]
        what_f: str = "|"
        res = gen_table(full_formula, glued_formula, what_f)
        self.assertEqual(res.rows[0], ['!c', 'x', 'x', 'x', 'x', ' '])
        self.assertEqual(res.rows[1], ['a|b', ' ', ' ', ' ', 'x', 'x'])

    def test_minimisation_sdnf(self):
        formula = "(a&b)->c"
        lf = LogicalFunction(formula)
        lf.to_rpn()
        lf.evaluate_rpn()
        sdnf = lf.sdnf()

        res = make_solvable(glue_formula_steps(split_str_formula(sdnf)), operation="|")
        self.assertEqual(res, "(!a)&(!b)&(c)")

    def test_minimisation_sknf(self):
        formula = "(a&b)->c"
        lf = LogicalFunction(formula)
        lf.to_rpn()
        lf.evaluate_rpn()
        sknf = lf.sknf()

        res = make_solvable(glue_formula_steps(split_str_formula(sknf)), operation="&")
        self.assertEqual(res, "(!a&!b&c)")


if __name__ == '__main__':
    unittest.main()
