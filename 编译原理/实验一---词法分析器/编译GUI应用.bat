@echo off

REM 检查Visual Studio命令提示符是否已启动
where cl >nul 2>nul
if %errorlevel% neq 0 (
    echo 请先打开Visual Studio命令提示符再运行此脚本！
    pause
    exit /b 1
)

REM 检查源文件是否存在
if not exist "main.cpp" (
    echo 找不到 main.cpp 文件！
    pause
    exit /b 1
)

if not exist "lexer.cpp" (
    echo 找不到 lexer.cpp 文件！
    pause
    exit /b 1
)

if not exist "lexer.h" (
    echo 找不到 lexer.h 文件！
    pause
    exit /b 1
)

REM 编译为GUI应用程序，使用/subsystem:windows选项
REM 这将创建一个没有控制台窗口的纯GUI应用程序
echo 开始编译词法分析器(GUI版本)...
cl /EHsc /D "WIN32" /D "_WINDOWS" /D "_UNICODE" /D "UNICODE" /Fe词法分析器.exe /link /subsystem:windows main.cpp lexer.cpp user32.lib

if %errorlevel% neq 0 (
    echo 编译失败！
    pause
    exit /b 1
) else (
    echo 编译成功！词法分析器.exe 已生成。
    echo 这是一个纯图形界面应用程序，双击即可运行。
    pause
)