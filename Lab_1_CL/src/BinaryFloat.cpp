#include "BinaryFloat.h"
#include <iostream>

BinaryFloat::BinaryFloat(float decimalNumber) {
    this->decimalNumber = decimalNumber;
    this->convertDecimalToBinary();
}

std::string BinaryFloat::wholeToBin(int whole) {
    std::string wholeBin;
    while (whole > 0) {
        wholeBin.insert(0, 1, std::to_string(whole % 2)[0]);
        whole /= 2;
    }
    return wholeBin;
}

// Преобразование десятичного числа в двоичный код IEEE-754
void BinaryFloat::convertDecimalToBinary() {
    // Определение знака
    sign = decimalNumber < 0;
    if (sign)
        decimalNumber *= (-1);

    // Представление специальных значений(0, +-inf, NaN)
    if (decimalNumber >= std::numeric_limits<float>::infinity()) {   //infinity
        exponent = "11111111";
        mantissa.append(23, '0');
        return;
    } else if (decimalNumber != decimalNumber) {   //NaN
        exponent = "11111111";
        mantissa = '1';
        mantissa.append(22, '0');
        return;
    } else if (decimalNumber == 0.0f) {   //NaN
        exponent = "00000000";
        mantissa.append(23, '0');
        return;
    }

    // Преобразовать целую часть в двоичное представление
    int whole = static_cast<int>(fabsf(decimalNumber));
    float fraction = fabsf(decimalNumber) - (float) whole;
    std::string wholeBin = wholeToBin(whole);
    std::string fractionBin;

    while (fractionBin.length() < 23 * 2) {
        fractionBin += std::to_string((int) (fraction *= 2));
        fraction >= 1 ? fraction-- : fraction;
    }


    // Определить экспоненту и мантиссу
    int exp = 0;
    if (!wholeBin.empty())
        while (wholeBin.length() != 1) {
            fractionBin.insert(0, 1, ((wholeBin[wholeBin.length() - 1])));
            wholeBin.pop_back();
            exp++;
        }
    else {
        while (!fractionBin.starts_with("1")) {
            fractionBin.erase(0, 1);
            exp--;
        }
        fractionBin.erase(0, 1);
        exp--;
    }


    while (fractionBin.length() > 23) {
        fractionBin.pop_back();
    }
    while (fractionBin.length() < 23) {
        fractionBin.append("0");
    }

    exponent = wholeToBin(127 + exp);
    while (exponent.length() < 8) {
        exponent.insert(0, "0");
    }
    mantissa = fractionBin;
    getStoredFloat();
}

// Получение двоичного представления
std::string BinaryFloat::getBinaryRepresentation() {
    std::string binaryRepresentation;
    binaryRepresentation += (sign ? "1" : "0") + exponent + mantissa;
    return binaryRepresentation;
}

float BinaryFloat::getStoredFloat() {
    int exp = 0;
    for (int i = 7; i >= 0; i--)
        exp += std::pow(2, 7 - i) * (exponent[i] == '1' ? 1 : 0);
    exp -= 127;
    //std::cout << exp << std::endl;
    if (exp == -127)
        storedNumber = 0;
    else if (exp >= 0) {
        std::string wholeBin;
        std::string fractionalBin;
        wholeBin = "1";
        for (int i = 0; i < exp; i++) {
            wholeBin += mantissa[i];
        }
        for (int i = exp; i < mantissa.length(); i++) {
            fractionalBin += mantissa[i];
        }
        int whole = 0;
        for (int i = wholeBin.length() - 1; i >= 0; i--)
            whole += std::pow(2, wholeBin.length() - 1 - i) * (wholeBin[i] == '1' ? 1 : 0);
        float fractional = 0;
        for (int i = 0; i < fractionalBin.length(); i++)
            fractional += std::pow(2, -(i + 1)) * (fractionalBin[i] == '1' ? 1 : 0);
        storedNumber = whole + fractional;

    } else {
        std::string fractionalBin = mantissa;
        fractionalBin.insert(0, "1");
        exp++;
        while (exp != 0) {
            fractionalBin.insert(0, "0");
            exp++;
        }
        float fractional = 0;
        for (int i = 0; i < fractionalBin.length(); i++)
            fractional += std::pow(2, -(i + 1)) * (fractionalBin[i] == '1' ? 1 : 0);
        storedNumber = fractional;
    }
    //std::cout << std::setprecision(24) << storedNumber;
    return storedNumber;
}

BinaryFloat BinaryFloat::operator+(BinaryFloat second) {
    BinaryFloat result(0);
    int firstExp = 0;
    for (int i = 7; i >= 0; i--)
        firstExp += std::pow(2, 7 - i) * (exponent[i] == '1' ? 1 : 0);
    firstExp -= 127;
    int secondExp = 0;
    for (int i = 7; i >= 0; i--)
        secondExp += std::pow(2, 7 - i) * (second.exponent[i] == '1' ? 1 : 0);
    secondExp -= 127;
    std::string firstMantissa = mantissa;
    std::string secondMantissa = second.mantissa;
    if (firstExp > secondExp) {
        secondMantissa.insert(0, "1");
        secondExp++;
        while (secondExp < firstExp) {
            secondExp++;
            secondMantissa.insert(0, "0");
        }
    } else if (secondExp > firstExp) {
        firstMantissa.insert(0, "1");
        firstExp++;
        while (firstExp < secondExp) {
            firstExp++;
            firstMantissa.insert(0, "0");
        }
    }
    while (firstMantissa.length() > secondMantissa.length()) {
        secondMantissa.push_back('0');
    }
    while (secondMantissa.length() > firstMantissa.length()) {
        firstMantissa.push_back('0');
    }
    bool expPlus = false;
    for (int i = firstMantissa.length() - 1; i >= 0; i--) {
        if (firstMantissa[i] == '1' && secondMantissa[i] == '1') {
            firstMantissa[i] = '0';
            expPlus = plusBit(firstMantissa, i - 1);
        } else if (firstMantissa[i] == '0' && secondMantissa[i] == '0') {
            firstMantissa[i] = '0';
        } else
            firstMantissa[i] = '1';
    }
    if (expPlus) {
        firstMantissa.insert(0, "0");
        firstExp++;
    }
    while (firstMantissa.length() > 23)
        firstMantissa.pop_back();
    result.mantissa = firstMantissa;
    result.exponent = wholeToBin(firstExp + 127);
    while (result.exponent.length() < 8) {
        result.exponent.insert(0, "0");
    }
    result.getStoredFloat();
    result.decimalNumber = this->decimalNumber + second.decimalNumber;
    return result;
}

bool BinaryFloat::plusBit(std::string &bitStr, int bitPosition) {
    if (bitPosition >= 0) {
        if (bitStr[bitPosition] == '0')
            bitStr[bitPosition] = '1';
        else {
            bitStr[bitPosition] = '0';
            bitPosition--;
            plusBit(bitStr, bitPosition);
        }
        return false;
    } else
        return true;

}
