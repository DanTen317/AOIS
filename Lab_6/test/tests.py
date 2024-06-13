import unittest
from HashTable import HashTable
from Hash import Hash


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.table = HashTable()

    def test_new_item(self):
        self.table.add("Антон")
        self.assertEqual(self.table.table[0].keyword_value, 0)
        self.assertEqual(self.table.table[0].keyword, "Антон")

    def test_new_item_duplicate(self):
        self.test_new_item()
        self.table.add("Антон")
        self.assertEqual(len(self.table.table), 1)

    def test_new_item_same_keyword_value(self):
        self.test_new_item()
        self.table.add("Атон")
        self.assertEqual(self.table.table[1].keyword_value, 1)
        self.assertEqual(self.table.table[1].keyword, "Атон")

    def test_remove_item(self):
        self.test_new_item()
        self.test_new_item_same_keyword_value()
        self.table.delete("Антон")
        self.assertEqual(len(self.table.table), 1)
        self.assertEqual(self.table.table[0].keyword_value, 0)
        self.assertEqual(self.table.table[0].keyword, "Атон")

    def test_update_item(self):
        self.test_new_item()
        self.assertEqual(self.table.table[0].keyword, "Антон")
        self.assertEqual(self.table.table[0].value, "")
        self.table.update("Антон", "описание")
        self.assertEqual(self.table.table[0].value, "описание")
        self.table.update("ппп", "описание")
        self.assertEqual(len(self.table.table), 1)


if __name__ == '__main__':
    unittest.main()
