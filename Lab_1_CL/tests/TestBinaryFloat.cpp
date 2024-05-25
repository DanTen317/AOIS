#include <gtest/gtest.h>
#include "../src/BinaryFloat.h"


TEST(TestFloatCreation, ZeroCreation) {
    BinaryFloat num(0);
    EXPECT_EQ(num.getBinaryRepresentation(), "00000000000000000000000000000000");
}

TEST(TestFloatCreation, infCreation) {
    BinaryFloat num(std::numeric_limits<float>::infinity());
    EXPECT_EQ(num.getBinaryRepresentation(), "01111111100000000000000000000000");
}

TEST(TestFloatCreation, NormalPositiveCreation) {
    BinaryFloat num(7.125);
    EXPECT_EQ(num.getBinaryRepresentation(), "01000000111001000000000000000000");
}

TEST(TestFloatCreation, NormalNegativeCreation) {
    BinaryFloat num(-7.625);
    EXPECT_EQ(num.getBinaryRepresentation(), "11000000111101000000000000000000");
}

TEST(TestFloatCreation, NormalCreation) {
    BinaryFloat num(0.0122);
    EXPECT_EQ(num.getBinaryRepresentation(), "00111100010001111110001010000010");
}

TEST(TestFloatSummary, SummaryFloat) {
    BinaryFloat num1(6.125);
    BinaryFloat num2(1.5);
    BinaryFloat res(0);
    res = num1 + num2;
    EXPECT_EQ(res.decimalNumber, 7.625);
    EXPECT_EQ(res.getBinaryRepresentation(), "01000000111101000000000000000000");
}

TEST(TestFloatSummary, SummaryFloatNegative) {
    BinaryFloat num1(-6.125);
    BinaryFloat num2(1.5);
    BinaryFloat res(0);
    res = num1 + num2;
    EXPECT_EQ(res.decimalNumber, 0);
    EXPECT_EQ(res.getBinaryRepresentation(), "00000000000000000000000000000000");
}

TEST(TestFloatSummary, SummaryFloat1) {
    BinaryFloat num1(1.125);
    BinaryFloat num2(6.5);
    BinaryFloat res(0);
    res = num1 + num2;
    EXPECT_EQ(res.decimalNumber, 7.625);
    EXPECT_EQ(res.getBinaryRepresentation(), "01000000111101000000000000000000");
}
TEST(TestFloatSummary, SummaryFloat2) {
    BinaryFloat num1(1.125);
    BinaryFloat num2(0.125);
    BinaryFloat res(0);
    res = num1 + num2;
    EXPECT_EQ(res.decimalNumber, 1.25);
    EXPECT_EQ(res.getBinaryRepresentation(), "00111111101000000000000000000000");
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}