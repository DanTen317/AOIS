#ifndef LAB_1_CL_BINARYINTEGER_H
#define LAB_1_CL_BINARYINTEGER_H

#include <string>

class BinaryInteger {
private:
public:
    int decimalNumber{};
    std::string binaryDirect;           //прямой код
    std::string binaryReverse;          //обратный код
    std::string binaryAdditional;       //дополнительный код

    BinaryInteger();

private:
    void makeBinaryDirect();

    void makeBinaryReverse();

    void makeBinaryAdditional();

    void makeDecimal();

    BinaryInteger makeNegative() const;

    bool getSignBit() const;

    bool getSignBit(BinaryInteger &) const;

    static std::string reverseString(std::string basicString);

    void addDigitsForMultipl(int);

    void makeOtherForms();

    void plusBitForAdditional(int bitPosition);

    void minusBitForReverse(int bitPosition);


public:
    explicit BinaryInteger(int);

    BinaryInteger operator+(const BinaryInteger &) const;

    BinaryInteger operator-(const BinaryInteger &) const;

    BinaryInteger operator*(BinaryInteger &) const;

    std::string operator/(BinaryInteger &) const;
};


#endif //LAB_1_CL_BINARYINTEGER_H
