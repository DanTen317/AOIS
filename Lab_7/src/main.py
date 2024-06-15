from double_matrix import Matrix
import numpy as np


def main():
    m = Matrix(size=16)
    print(np.matrix(m.matrix))
    print("Word:", m.read_word(1))
    print("Address column:", m.get_address_column(3))

    m.summarize_a_b("111")
    print(np.matrix(m.matrix))

    print("Operations:")
    m.operations(0, 1, 14, operation="OR")
    m.operations(0, 1, 15, operation="OR-NOT")
    m.operations(0, 1, operation="NO F")
    m.operations(0, 1, operation="NOT-NO FS")

    print(np.matrix(m.matrix))

    m.find_words_from_interval("0100000000000000", "1111111111111111")


if __name__ == '__main__':
    main()
