#!/bin/bash
echo "正在编译词法分析器..."
g++ -std=c++11 main.cpp lexer.cpp -o 词法分析器
if [ $? -eq 0 ]; then
    echo "编译成功！"
    echo ""
    echo "使用方法："
    echo "  ./词法分析器 program1.txt"
else
    echo "编译失败，请检查是否安装了g++编译器"
fi

