#include "gtest/gtest.h"
#include "../src/BinaryInteger.h"

TEST(TestIntCreation, ZeroCreation) {
    BinaryInteger num(0);
    EXPECT_EQ(num.binaryDirect,"00000000");
    EXPECT_EQ(num.binaryReverse,"00000000");
    EXPECT_EQ(num.binaryAdditional,"00000000");
}

TEST(TestIntCreation, NormalPositiveCreation) {
    BinaryInteger num(2);
    EXPECT_EQ(num.binaryDirect,"00000010");
    EXPECT_EQ(num.binaryReverse,"00000010");
    EXPECT_EQ(num.binaryAdditional,"00000010");
}

TEST(TestIntCreation, NormalNegativeCreation) {
    BinaryInteger num(-2);
    EXPECT_EQ(num.binaryDirect,"10000010");
    EXPECT_EQ(num.binaryReverse,"11111101");
    EXPECT_EQ(num.binaryAdditional,"11111110");
}

TEST(TestIntOperations,TestSummary){
    BinaryInteger num1(2);
    BinaryInteger num2(6);
    BinaryInteger res(0);
    res = num1+num2;
    EXPECT_EQ(res.decimalNumber,8);
    EXPECT_EQ(res.binaryDirect, "00001000");
}

TEST(TestIntOperations,TestSummaryNeg){
    BinaryInteger num1(2);
    BinaryInteger num2(-6);
    BinaryInteger res(0);
    res = num1+num2;
    EXPECT_EQ(res.decimalNumber,-4);
    EXPECT_EQ(res.binaryDirect, "10000100");
}

TEST(TestIntOperations,TestMultiply){
    BinaryInteger num1(2);
    BinaryInteger num2(6);
    BinaryInteger res(0);
    res = num1*num2;
    EXPECT_EQ(res.decimalNumber,12);
    EXPECT_EQ(res.binaryDirect, "00001100");
}

TEST(TestIntOperations,TestMinus){
    BinaryInteger num1(6);
    BinaryInteger num2(2);
    BinaryInteger res(0);
    res = num1-num2;
    EXPECT_EQ(res.decimalNumber,4);
    EXPECT_EQ(res.binaryDirect, "00000100");
}

TEST(TestIntOperations,TestDivision){
    BinaryInteger num1(6);
    BinaryInteger num2(4);
    BinaryInteger res(0);
    EXPECT_EQ(num1/num2,"00000001.10000");
}