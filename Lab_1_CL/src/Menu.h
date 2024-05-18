#ifndef LAB_1_CL_MENU_H
#define LAB_1_CL_MENU_H

#include <iostream>
#include <conio.h>
#include <string>
#include <iomanip>
#include <thread>

#include "Exceptions.h"
#include "BinaryFloat.h"


using namespace std::chrono_literals;

int getDecimal(bool);

void makeNumber(BinaryInteger &, BinaryInteger &);

void showInfo(BinaryInteger &);

void Operation(BinaryInteger &, BinaryInteger &);

void Operation(BinaryInteger &first, BinaryInteger &second) {
    std::cout << R"(Write "+" "-" "*" "/")" << std::endl;
    char option;
    std::string res;
    std::cin >> option;
    BinaryInteger result;

    switch (option) {
        case '+':
            result = first + second;
            std::cout << result.decimalNumber << std::endl << result.binaryDirect << std::endl
                      << result.binaryReverse << std::endl << result.binaryAdditional << std::endl;
            break;
        case '-':
            result = first - second;
            std::cout << result.decimalNumber << std::endl << result.binaryDirect << std::endl
                      << result.binaryReverse << std::endl << result.binaryAdditional << std::endl;
            break;
        case '*':
            result = first * second;
            std::cout << result.decimalNumber << std::endl << result.binaryDirect << std::endl
                      << result.binaryReverse << std::endl << result.binaryAdditional << std::endl;
            break;
        case '/':
            res = first / second;
            std::cout << res << std::endl;
            break;
        default:
            std::cerr << "Wrong operation\n";
            std::this_thread::sleep_for(100ms);
            std::cin.clear();
            std::rewind(stdin);
            break;
    }
}

void showInfo(BinaryInteger &number) {
    std::cout << number.binaryDirect << std::endl;
    std::cout << number.binaryReverse << std::endl;
    std::cout << number.binaryAdditional << std::endl;
}


void menu(BinaryInteger &first, BinaryInteger &second) {
    std::string option;
    bool exitAll = false;
    bool exit = false;
    BinaryFloat firstFloat(0);
    BinaryFloat secondFloat(0);
    BinaryFloat resultFloat(0);
    float input;
    while (!exitAll) {
        std::cout << "i - Int\nf - Float\nother - exit\n";
        std::cin >> option;
        option[0] = option.length() > 1 ? 0 : option[0];
        switch (option[0]) {
            case 'f':
                std::cout << "Input first float:";
                std::cin >> input;
                firstFloat = BinaryFloat(input);
                std::cout << "Input first float:";
                std::cin >> input;
                secondFloat = BinaryFloat(input);
                std::cout << "First:\n"
                             "decimal:" << firstFloat.decimalNumber << std::endl <<
                          "binary:" << firstFloat.getBinaryRepresentation() << std::endl <<
                          "stored float:" << std::setprecision(24) << firstFloat.storedNumber << std::endl;
                std::cout << "Second:\n"
                             "decimal:" << secondFloat.decimalNumber << std::endl <<
                          "binary:" << secondFloat.getBinaryRepresentation() << std::endl <<
                          "stored float:" << std::setprecision(24) << secondFloat.storedNumber << std::endl;
                resultFloat = firstFloat + secondFloat;
                std::cout << "summary:\n"
                             "decimal:" << resultFloat.decimalNumber << std::endl <<
                          "binary:" << resultFloat.getBinaryRepresentation() << std::endl <<
                          "stored float:" << std::setprecision(24) << resultFloat.storedNumber << std::endl;
                break;
            case 'i':
                while (!exit) {
                    std::cout << "-------------------------\n"
                                 "1 - to make/remake number\n"
                                 "2 - to chose an operation\n"
                                 "3 - to print info\n"
                                 "0 or other - to exit\n"
                                 "-------------------------\n";
                    std::cin >> option;
                    //std::cin.clear();
                    //std::rewind(stdin);
                    option[0] = option.length() > 1 ? 0 : option[0];
                    switch (option[0]) {
                        default:
                        case '0':
                            exit = true;
                            break;
                        case '1':
                            makeNumber(first, second);
                            break;
                        case '2':
                            Operation(first, second);
                            break;
                        case '3':
                            std::cout << "First number:\n";
                            showInfo(first);
                            std::cout << "\nSecond number:\n";
                            showInfo(second);
                            std::cout << std::endl;
                            break;
                    }

                }
                break;
            default:
                exitAll = true;
                break;
        }
    }
}

void makeNumber(BinaryInteger &firstNum, BinaryInteger &secondNum) {
    std::cout << "Choose number (1/2) to replace:\n";
    std::string option;
    std::cin >> option;
    //std::cin.clear();
    //std::rewind(stdin);
    option[0] = option.length() > 1 ? 0 : option[0];
    bool passConstructor;
    passConstructor = !(option == "1" || option == "2");
    BinaryInteger newNum(getDecimal(passConstructor));
    switch (option[0]) {
        case '1':
            firstNum = newNum;
            break;
        case '2':
            secondNum = newNum;
            break;
        default:
            std::cerr << "Wrong number chosen. Nothing changed\n";
            std::this_thread::sleep_for(100ms);
            break;
    }
}

int getDecimal(bool pass) {
    int decimal;
    while (!pass) {
        try {
            std::cout << "Enter decimal:";
            std::cin >> decimal;
            if (std::cin.fail() || (std::cin.peek() != '\n' && std::cin.peek() != ' ')) {
                throw WrongValue("Not digit");
            }
            if (decimal > 127 || decimal < -128)
                throw WrongValue("Must be [-128, 127]");
            return decimal;
        }
        catch (const WrongValue &err) {
            std::cerr << err.what();
            std::this_thread::sleep_for(100ms);
            std::cout << "Press any button to try again\n";
            getch();
            rewind(stdin);
            std::cin.clear();
        }
    }
    return NULL;
}

#endif //LAB_1_CL_MENU_H
