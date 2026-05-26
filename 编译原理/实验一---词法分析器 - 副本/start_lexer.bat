@echo off

REM Check if lexer.exe exists
if not exist "词法分析器.exe" (
    echo Cannot find 词法分析器.exe! Please compile first.
    echo Run "编译GUI应用.bat" to compile.
    pause
    exit /b 1
)

REM Start the lexer GUI application
echo Starting Lexical Analyzer GUI...
start "词法分析器" "词法分析器.exe"
echo Lexical Analyzer started. Please check the program window.
pause