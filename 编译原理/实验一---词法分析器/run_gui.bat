@echo off

REM 检查词法分析器.exe是否存在
if not exist "词法分析器.exe" (
    echo 找不到词法分析器.exe，请先编译程序！
    echo 请运行"编译GUI应用.bat"来编译程序。
    pause
    exit /b 1
)

REM 启动GUI版本的词法分析器
echo 启动词法分析器图形界面...
start "词法分析器" "词法分析器.exe"
echo 词法分析器已启动，请查看程序窗口。
pause