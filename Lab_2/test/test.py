import unittest
from logical_function import *


class TestLogicalFunction(unittest.TestCase):

    def test_process_input(self):
        self.assertTrue(process_input("a&b"))
        self.assertTrue(process_input("!a|b"))
        self.assertTrue(process_input("(a->b)"))
        self.assertTrue(process_input("a~b"))
        self.assertFalse(process_input("a$b"))
        self.assertFalse(process_input("a&b)"))
        self.assertFalse(process_input("a&(b"))

    def test_rpn_conversion(self):
        lf = LogicalFunction("a&b")
        lf.to_rpn()
        self.assertEqual(lf.rpn, "ab&")

        lf = LogicalFunction("a|b")
        lf.to_rpn()
        self.assertEqual(lf.rpn, "ab|")

        lf = LogicalFunction("a->b")
        lf.to_rpn()
        self.assertEqual(lf.rpn, "ab>")

        lf = LogicalFunction("(a|b)&c")
        lf.to_rpn()
        self.assertEqual(lf.rpn, "ab|c&")

    def test_evaluate_rpn(self):
        lf = LogicalFunction("a&b")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.res_dict['a'], [0, 0, 1, 1])
        self.assertEqual(lf.res_dict['b'], [0, 1, 0, 1])
        self.assertEqual(lf.res_dict['& (1)'], [0, 0, 0, 1])

        lf = LogicalFunction("a|b")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.res_dict['| (1)'], [0, 1, 1, 1])

    def test_evaluate_rpn_2(self):
        lf = LogicalFunction("(!a&b)")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.res_dict['a'], [0, 0, 1, 1])
        self.assertEqual(lf.res_dict['b'], [0, 1, 0, 1])
        self.assertEqual(lf.res_dict['! (1)'], [1, 1, 0, 0])
        self.assertEqual(lf.res_dict['& (2)'], [0, 1, 0, 0])

        lf = LogicalFunction("(a->b)~a")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.res_dict['a'], [0, 0, 1, 1])
        self.assertEqual(lf.res_dict['b'], [0, 1, 0, 1])
        self.assertEqual(lf.res_dict['-> (1)'], [1, 1, 0, 1])
        self.assertEqual(lf.res_dict['~ (2)'], [0, 0, 0, 1])

    def test_sdnf(self):
        lf = LogicalFunction("a&b")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.sdnf(), "(a&b)")

    def test_sknf(self):
        lf = LogicalFunction("a&b")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.sknf(), "(a|b)&(a|!b)&(!a|b)")

    def test_num_sdnf(self):
        lf = LogicalFunction("a&b")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.num_sdnf(), "(3) |")

    def test_num_sknf(self):
        lf = LogicalFunction("a&b")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.num_sknf(), "(0, 1, 2) &")

    def test_index_form(self):
        lf = LogicalFunction("a&b")
        lf.to_rpn()
        lf.evaluate_rpn()
        self.assertEqual(lf.index_form(), "0001 - 1")


if __name__ == '__main__':
    unittest.main()
