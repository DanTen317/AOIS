#include <iostream>
#include "src/BinaryInteger.h"
#include "src/Menu.h"


int main() {
    BinaryInteger num1;
    BinaryInteger num2;
    menu(num1, num2);

    //BinaryFloat(11.75);

    return 0;
}

//int main() {
//    float decimalNumber;
//    std::cout << "Floating point decimal number:";
//    std::cin >> decimalNumber;
//
//    BinaryFloat binaryFloat(decimalNumber);
//    std::cout << binaryFloat.sign << " " << binaryFloat.exponent << " ." << binaryFloat.mantissa << std::endl;
//    std::cout << binaryFloat.getBinaryRepresentation() << std::endl;
//
//    std::cout << std::setprecision(24) << binaryFloat.getStoredFloat() << std::endl;
//
//    BinaryFloat b1(10.2);
//    BinaryFloat b2(0.25);
//    BinaryFloat result(0);
//    result = b1 + b2;
//    std::cout << result.getBinaryRepresentation() << std::endl;
//    std::cout << std::setprecision(24) << result.getStoredFloat() << std::endl;
//
//
//    return 0;
//}