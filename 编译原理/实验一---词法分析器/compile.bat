@echo off
chcp 65001 >nul
echo 正在编译词法分析器...

REM 尝试直接编译
cl /EHsc main.cpp lexer.cpp user32.lib /Fe词法分析器.exe

if %errorlevel% == 0 (
    echo 编译成功！
    echo.
    echo 使用方法：
    echo   双击 词法分析器.exe 运行图形界面版本
) else (
    echo 编译失败，请按照以下步骤手动编译：
    echo 1. 打开Visual Studio命令提示符（Developer Command Prompt）
    echo    - 方法1：在开始菜单中搜索 "Developer Command Prompt"
    echo    - 方法2：在Visual Studio中，选择 工具 > 命令行 > Developer Command Prompt
    echo 2. 在命令提示符中，导航到当前目录：
    echo    cd "%cd%"
    echo 3. 运行以下命令：
    echo    cl /EHsc main.cpp lexer.cpp user32.lib /Fe词法分析器.exe
    echo 4. 编译成功后，双击生成的词法分析器.exe文件
)
pause

