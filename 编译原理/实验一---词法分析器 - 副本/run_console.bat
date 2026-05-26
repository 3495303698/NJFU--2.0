@echo off
chcp 65001 >nul

echo ========================================
echo 词法分析器控制台版本运行脚本
echo ========================================

echo.
echo 请选择要分析的测试文件：
echo 1. program1.txt
echo 2. program2.txt
echo 3. program3.txt
echo.

choice /c 123 /m "请选择文件"
if %errorlevel% == 1 set INPUT_FILE=program1.txt
if %errorlevel% == 2 set INPUT_FILE=program2.txt
if %errorlevel% == 3 set INPUT_FILE=program3.txt

echo.
echo 运行词法分析器...
echo 分析文件: %INPUT_FILE%
echo.

if exist "词法分析器_simple.exe" (
    echo 使用已编译的控制台版本...
    cmd /c "词法分析器_simple.exe" %INPUT_FILE%
) else (
    echo 未找到预编译的控制台版本，尝试使用GUI版本...
    if exist "词法分析器.exe" (
        start "" "词法分析器.exe"
        echo GUI版本已启动，请在弹出的窗口中操作
    ) else (
        echo 错误：未找到可执行文件，请先编译程序
        goto end
    )
)

echo.
echo 程序执行完毕，按任意键退出...
:end
pause >nul