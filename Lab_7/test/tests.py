import unittest
from src.double_matrix import Matrix


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = Matrix()

    def set_zero_matrix(self):
        for i in range(self.m.size):
            for j in range(self.m.size):
                self.m.matrix[i][j] = 0
        print(self.m.matrix)

    def test_matrix_get_word(self):
        self.set_zero_matrix()
        self.m.matrix[0][0] = 1
        res = self.m.read_word(0)
        self.assertEqual(res, "1000000000000000")

    def test_matrix_get_word_exception(self):
        res = self.m.read_word(16)
        self.assertEqual(res, False)

    def test_matrix_get_address_column(self):
        self.set_zero_matrix()
        self.m.matrix[1][0] = 1
        self.m.matrix[0][15] = 1
        res = self.m.get_address_column(1)
        self.assertEqual(res, "1000000000000001")

    def test_matrix_get_address_column_exception(self):
        self.set_zero_matrix()
        self.m.matrix[1][0] = 1
        self.m.matrix[0][15] = 1
        res = self.m.get_address_column(17)
        self.assertEqual(res, False)

    def test_matrix_summ(self):
        self.set_zero_matrix()
        self.m.matrix[0][0] = 1
        self.m.matrix[15][0] = 1
        self.m.matrix[3][0] = 1
        self.m.summarize_a_b("100")
        self.assertEqual(self.m.matrix[12][0], 1)
        self.assertEqual(self.m.matrix[15][0], 0)

    def test_matrix_summ_2(self):
        self.set_zero_matrix()
        self.m.matrix[2][2] = 1
        self.m.matrix[1][2] = 1
        self.m.matrix[5][2] = 1
        self.m.summarize_a_b("100")
        self.assertEqual(self.m.matrix[14][2], 1)
        self.assertEqual(self.m.matrix[1][2], 0)

    def test_matrix_summ_exception(self):
        res = self.m.summarize_a_b("11111")
        self.assertEqual(res, False)
        res = self.m.summarize_a_b("1d1")
        self.assertEqual(res, False)

    def test_matrix_operation_disjunction(self):
        self.set_zero_matrix()
        self.m.matrix[0][0] = 1
        self.m.matrix[1][1] = 1
        self.m.operations(0, 1, 15, "OR")
        self.assertEqual(self.m.matrix[15][15], 1)
        for i in range(self.m.size - 1):
            self.assertEqual(self.m.matrix[i][15], 0)

    def test_matrix_operation_piers(self):
        self.set_zero_matrix()
        self.m.matrix[0][0] = 1
        self.m.matrix[1][1] = 1
        self.m.operations(0, 1, 15, "OR-NOT")
        self.assertEqual(self.m.matrix[15][15], 0)
        for i in range(self.m.size - 1):
            self.assertEqual(self.m.matrix[i][15], 1)

    def test_matrix_operation_not_first(self):
        self.set_zero_matrix()
        self.m.matrix[0][0] = 1
        self.m.matrix[1][1] = 0
        self.m.operations(0, 1, 15, "NO F")
        self.assertEqual(self.m.matrix[15][15], 1)
        for i in range(self.m.size - 1):
            self.assertEqual(self.m.matrix[i][15], 0)

    def test_matrix_operation_implication(self):
        self.set_zero_matrix()
        self.m.matrix[0][0] = 1
        self.m.matrix[1][1] = 0
        self.m.operations(0, 1, 15, "NOT-NO FS")
        self.assertEqual(self.m.matrix[15][15], 0)
        for i in range(self.m.size - 1):
            self.assertEqual(self.m.matrix[i][15], 1)

    def test_matrix_find(self):
        self.set_zero_matrix()
        self.m.matrix[0][0] = 1
        self.m.matrix[3][3] = 1
        self.m.matrix[1][3] = 1
        res = self.m.find_words_from_interval("0000000000000001","1000000000000000")
        self.assertEqual(res, ["1000000000000000"])


if __name__ == '__main__':
    unittest.main()
