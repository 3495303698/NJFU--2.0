@echo off
REM Windows 批处理编译脚本

echo 正在编译递归下降分析程序...

REM 使用 g++ 编译（如果已安装 MinGW 或 MSYS2）
g++ -Wall -std=c++11 -I include src/main.cpp src/parser.cpp -o parser.exe

if %errorlevel% equ 0 (
    echo 编译成功！
    echo 运行 parser.exe 来使用程序
) else (
    echo 编译失败，请检查是否安装了 g++ 编译器
    echo 或者使用 Visual Studio 的 cl.exe 编译器
)

pause
