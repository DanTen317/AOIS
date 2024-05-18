#include <iostream>
#include <string>
#include <cmath>
#include <limits>

class BinaryFloat {
public:
    float decimalNumber;
    bool sign;
    std::string exponent;
    std::string mantissa;
    float storedNumber;

public:
    BinaryFloat(float);

    std::string wholeToBin(int);

    void convertDecimalToBinary();

    std::string getBinaryRepresentation();

    float getStoredFloat();

    BinaryFloat operator+(BinaryFloat);

private:
    bool plusBit(std::string &, int);
};