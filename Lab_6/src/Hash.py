class Hash:
    def __init__(self, keyword: str, value: str = ""):
        self.__alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.keyword = keyword
        self.value = value
        self.keyword_value = 0
        self.hash_address = 0
        self.__set_keyword_value()
        self.__set_hash_address()

    def __set_keyword_value(self):
        if (self.keyword[0] in self.__alphabet or
                self.keyword[0] in self.__alphabet.lower()):
            a = self.keyword[0]
            self.keyword_value = self.__alphabet.index(self.keyword[0].upper())
        else:
            raise ValueError("Keyword value must start with russian letter!")

    def __set_hash_address(self):
        self.hash_address = self.keyword_value % len(self.__alphabet)

    def __str__(self):
        return f"{self.keyword_value} | {self.keyword}: {self.value if self.value != "" else None}"
