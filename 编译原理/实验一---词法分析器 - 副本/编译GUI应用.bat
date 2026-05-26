@echo off
chcp 65001 >nul 2>nul
echo ==========================================
echo    词法分析器 GUI 版本编译脚本
echo ==========================================
echo.

REM 检查Visual Studio命令提示符是否已启动
where cl >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Visual Studio 编译环境！
    echo.
    echo 请按照以下步骤操作：
    echo.
    echo 1. 按 Windows 键，搜索 "Developer Command Prompt" 或 "开发人员命令提示符"
    echo 2. 打开 Visual Studio 命令提示符（不是普通命令提示符）
    echo 3. 在命令提示符中导航到当前目录：
    echo    cd /d "%cd%"
    echo 4. 再次运行此脚本：编译GUI应用.bat
    echo.
    echo 或者，如果您知道 Visual Studio 安装路径，可以手动设置环境：
    echo    "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    echo.
    pause
    exit /b 1
)

echo [√] 检测到 Visual Studio 编译环境
echo.

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
REM 添加comdlg32.lib以支持文件对话框功能
echo [*] 开始编译词法分析器(GUI版本)...
echo.
cl /EHsc /D "WIN32" /D "_WINDOWS" /D "_UNICODE" /D "UNICODE" /Fe词法分析器.exe /link /subsystem:windows main.cpp lexer.cpp user32.lib comdlg32.lib

if %errorlevel% neq 0 (
    echo.
    echo ==========================================
    echo [×] 编译失败！
    echo ==========================================
    echo.
    echo 可能的原因：
    echo 1. 源文件有语法错误
    echo 2. 缺少必要的库文件
    echo 3. Visual Studio 环境配置不完整
    echo.
    echo 请检查上方的错误信息，修复后重试。
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ==========================================
    echo [√] 编译成功！
    echo ==========================================
    echo.
    echo 生成的文件：词法分析器.exe
    echo.
    echo 使用方法：
    echo 1. 双击 "词法分析器.exe" 运行程序
    echo 2. 在图形界面中选择源文件进行分析
    echo 3. 查看分析结果并保存（可选）
    echo.
    echo ==========================================
    pause
)