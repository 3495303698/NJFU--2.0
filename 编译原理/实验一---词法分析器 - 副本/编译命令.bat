@echo off

REM 简单的词法分析器编译脚本
REM 注意：请在Visual Studio命令提示符中运行此脚本！

cls
echo ====================================================
echo         词法分析器编译脚本
REM 注意：请在Visual Studio命令提示符中运行此脚本！
echo ====================================================
echo.

REM 显示当前目录
echo 当前工作目录: %cd%
echo.

REM 检查源文件是否存在
if not exist main.cpp (
    echo 错误：找不到main.cpp文件！
    pause
    exit /b 1
)

if not exist lexer.cpp (
    echo 错误：找不到lexer.cpp文件！
    pause
    exit /b 1
)

if not exist lexer.h (
    echo 错误：找不到lexer.h文件！
    pause
    exit /b 1
)

REM 显示编译命令
echo 正在执行编译命令：
echo cl /EHsc /D "_UNICODE" /D "UNICODE" main.cpp lexer.cpp /Fe词法分析器.exe /link /subsystem:windows user32.lib comdlg32.lib
echo.

REM 执行编译命令 - GUI应用程序，添加文件对话框支持
cl /EHsc /D "_UNICODE" /D "UNICODE" main.cpp lexer.cpp /Fe词法分析器.exe /link /subsystem:windows user32.lib comdlg32.lib

REM 检查编译结果
if %errorlevel% equ 0 (
    echo.
    echo ====================================================
    echo 编译成功！
    echo 生成的可执行文件：词法分析器.exe
    echo 请直接运行：词法分析器.exe
    echo ====================================================
) else (
    echo.
    echo ====================================================
    echo 编译失败！
    echo 请确保您在Visual Studio命令提示符中运行此脚本
    echo 如果问题仍然存在，请尝试手动运行编译命令
    echo ====================================================
)

pause