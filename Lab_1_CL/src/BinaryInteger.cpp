#include "BinaryInteger.h"
#include "Exceptions.h"
#include <cmath>

BinaryInteger::BinaryInteger(int decimalNumber) : decimalNumber(decimalNumber) {
    try {
        if (decimalNumber > 127 || decimalNumber < -128)
            throw WrongValue("Must be [-128, 127]");
        else {
            makeBinaryDirect();
            makeBinaryReverse();
            makeBinaryAdditional();
        }
    }
    catch (const WrongValue &err) {
        std::cout << err.what();
    }

}

bool BinaryInteger::getSignBit() const {
    return decimalNumber < 0;
}

std::string BinaryInteger::reverseString(std::string stringToReverse) {
    std::string reversedString;
    for (size_t i = stringToReverse.length(); i > 0; i--) {
        reversedString += stringToReverse[i - 1];
    }
    return reversedString;
}

void BinaryInteger::makeBinaryDirect() {
    int decimal = abs(decimalNumber);
    std::string tempDirect;
    while (decimal >= 1) {
        tempDirect += (std::to_string(decimal % 2));
        decimal /= 2;
    }
    tempDirect += std::to_string(getSignBit());
    binaryDirect = reverseString(tempDirect);
    while (binaryDirect.length() < 8) {
        binaryDirect.insert(1, "0");
    }
}

void BinaryInteger::makeBinaryReverse() {
    if (binaryDirect[0] == '1') {
        binaryReverse += this->binaryDirect[0];
        for (int i = 1; i < binaryDirect.length(); i++) {
            if (binaryDirect[i] == '0') {
                binaryReverse += '1';
            } else {
                binaryReverse += '0';
            }
        }
    } else
        binaryReverse = binaryDirect;
}

void BinaryInteger::makeBinaryAdditional() {

    int bitPosition = binaryReverse.length() - 1;

    binaryAdditional = binaryReverse;
    if (binaryDirect[0] == '1')
        plusBitForAdditional(bitPosition);
}

void BinaryInteger::plusBitForAdditional(int bitPosition) {
    if (bitPosition >= 0) {
        if (binaryAdditional[bitPosition] == '0')
            binaryAdditional[bitPosition] = '1';
        else {
            binaryAdditional[bitPosition] = '0';
            bitPosition--;
            plusBitForAdditional(bitPosition);
        }
    }
}

void BinaryInteger::minusBitForReverse(int bitPosition) {
    if (bitPosition >= 0) {
        if (binaryReverse[bitPosition] == '1')
            binaryReverse[bitPosition] = '0';
        else {
            binaryReverse[bitPosition] = '1';
            bitPosition--;
            minusBitForReverse(bitPosition);
        }
    }
}

BinaryInteger BinaryInteger::operator+(const BinaryInteger &secondNumber) const {
    BinaryInteger resultNumber;
    resultNumber.binaryAdditional = this->binaryAdditional;
    for (int i = 7; i >= 0; i--) {
        if (resultNumber.binaryAdditional[i] == '1' && secondNumber.binaryAdditional[i] == '1') {
            resultNumber.binaryAdditional[i] = '0';
            resultNumber.plusBitForAdditional(i - 1);
        } else if (resultNumber.binaryAdditional[i] == '0' && secondNumber.binaryAdditional[i] == '0') {
            resultNumber.binaryAdditional[i] = '0';
        } else
            resultNumber.binaryAdditional[i] = '1';
    }

    resultNumber.makeOtherForms();
    return resultNumber;
}


BinaryInteger BinaryInteger::operator-(const BinaryInteger &secondNumber) const {
    BinaryInteger result;
    result.binaryAdditional = this->binaryAdditional;
    BinaryInteger second = secondNumber.makeNegative();
    result = result + second;
    result.makeOtherForms();
    return result;
}

BinaryInteger BinaryInteger::makeNegative() const {
    BinaryInteger negativeNumber;
    negativeNumber = *this;
    if (this->binaryDirect[0] == '0') {
        negativeNumber.binaryDirect[0] = '1';
    } else {
        negativeNumber.binaryDirect[0] = '0';
    }
    negativeNumber.binaryReverse.erase();
    negativeNumber.binaryAdditional.erase();
    negativeNumber.makeBinaryReverse();
    negativeNumber.makeBinaryAdditional();
    return negativeNumber;
}

void BinaryInteger::makeDecimal() {
    int decimal = 0;
    for (int i = 7; i > 0; i--)
        decimal += std::pow(2, 7 - i) * (binaryDirect[i] - '0');
    if (binaryDirect[0] == '1')
        decimal *= -1;
    this->decimalNumber = decimal;
}

BinaryInteger BinaryInteger::operator*(BinaryInteger &secondNumber) const {
    BinaryInteger resultNumber, firstNumber;
    resultNumber.binaryAdditional = std::string(8, '0');
    try {
        if (this->decimalNumber * secondNumber.decimalNumber > 127 ||
            this->decimalNumber * secondNumber.decimalNumber < -128)
            throw WrongValue("Result is \"" + std::to_string(decimalNumber * secondNumber.decimalNumber) +
                             "\", must be in [-128, 127]");
        bool isNegative = getSignBit(secondNumber);
        firstNumber.binaryDirect = this->binaryDirect;
        firstNumber.binaryDirect[0] = '0';
        firstNumber.makeBinaryReverse();
        firstNumber.makeBinaryAdditional();

        for (int i = 7; i > 0; i--) {
            if (secondNumber.binaryDirect[i] == '1') {
                BinaryInteger plusNumber = firstNumber;
                plusNumber.addDigitsForMultipl(i);
                resultNumber = resultNumber + plusNumber;
            }
        }
        resultNumber.binaryAdditional[0] = isNegative ? '1' : '0';
        resultNumber.binaryDirect.erase();
        resultNumber.binaryDirect = resultNumber.binaryAdditional;
        resultNumber.binaryAdditional.erase();

    }
    catch (const WrongValue &err) {
        std::cerr << err.what();
        //std::this_thread::sleep_for(100ms);
        rewind(stdin);
        std::cin.clear();
    }
    resultNumber.makeOtherForms();
    return resultNumber;
}

void BinaryInteger::addDigitsForMultipl(int digit) {
    this->binaryAdditional.insert(8, 7 - digit, '0');
    this->binaryAdditional.erase(0, this->binaryAdditional.length() - 8);
}

bool BinaryInteger::getSignBit(BinaryInteger &secondNumber) const {
    if (this->binaryDirect[0] == '1') {
        if (secondNumber.binaryDirect[0] == '0')
            return true;
        else
            return false;
    } else {
        if (secondNumber.binaryDirect[0] == '1')
            return true;
        else
            return false;
    }
}


std::string BinaryInteger::operator/(BinaryInteger &secondNumber) const {
    bool isNegative = getSignBit(secondNumber);
    if (secondNumber.decimalNumber == 0)
        throw WrongValue("Division by zero");

    BinaryInteger firstCopy(abs(decimalNumber));
    BinaryInteger tempNum(0);
    BinaryInteger wholePart(0);
    while (firstCopy.decimalNumber >= secondNumber.decimalNumber) {
        tempNum = firstCopy - secondNumber;
        firstCopy = tempNum;
        wholePart = wholePart + BinaryInteger(1);
    }
    int fractionalInt = 0;
    for (int i = firstCopy.binaryDirect.length() - 1; i >= 0; i--)
        fractionalInt += std::pow(2, 7 - i) * (firstCopy.binaryDirect[i] == '1' ? 1 : 0);

    float fraction = (float) fractionalInt / (float) secondNumber.decimalNumber;
    std::string fractionBin;

    while (fractionBin.length() < 5) {
        fractionBin += std::to_string((int) (fraction *= 2));
        fraction >= 1 ? fraction-- : fraction;
    }
    wholePart.binaryDirect[0] = isNegative ? '1' : '0';
    return wholePart.binaryDirect + "." + fractionBin;
}

void BinaryInteger::makeOtherForms() {
    if (!this->binaryAdditional.empty()) {
        if (this->binaryAdditional[0] == '0') {
            this->binaryDirect = this->binaryAdditional;
            this->binaryReverse = this->binaryAdditional;
            this->makeDecimal();
        } else {
            this->binaryReverse = binaryAdditional;
            this->minusBitForReverse(7);
            binaryDirect.erase();
            binaryDirect += "1";
            for (int i = 1; i < 8; i++) {
                binaryDirect += binaryReverse[i] == '0' ? '1' : '0';
            }
            this->makeDecimal();
        }
        return;
    }
    if (!this->binaryDirect.empty()) {
        this->makeDecimal();
        this->binaryReverse.erase();
        this->makeBinaryReverse();
        this->makeBinaryAdditional();
    }
}


BinaryInteger::BinaryInteger() = default;
