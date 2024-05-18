#ifndef LAB_1_CL_EXCEPTIONS_H
#define LAB_1_CL_EXCEPTIONS_H

#include <iostream>
#include <utility>

class WrongValue : public std::exception {
private:
    std::string message;
public:
    WrongValue(const std::string& message) : message(message) {}

    const char* what() const noexcept override {
        return message.c_str();
    }
};


#endif //LAB_1_CL_EXCEPTIONS_H
