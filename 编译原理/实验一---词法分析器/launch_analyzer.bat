@echo off

echo Launching Lexical Analyzer...
start "" analyzer.exe
if %errorlevel% neq 0 (
    echo Cannot launch the program!
    pause
    exit /b 1
)
echo Program launched successfully.
pause