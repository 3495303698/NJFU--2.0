@echo off
chcp 65001 >nul

echo ========================================
echo 词法分析器图形界面版本运行脚本
echo ========================================

echo.
echo 正在启动词法分析器图形界面版本...
echo.

if exist "词法分析器.exe" (
    start "" "词法分析器.exe"
    echo 词法分析器GUI版本已启动，请查看弹出的窗口。
) else (
    echo 错误：未找到词法分析器.exe 文件，请先编译程序。
    echo 请运行"编译GUI应用.bat"来编译程序。
    goto end
)

echo.
echo 程序已启动，此窗口将保持打开状态。
echo 如需关闭此窗口，请按任意键...
:end
pause >nul