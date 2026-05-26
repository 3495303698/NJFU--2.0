#include "lexer.h"
#include <windows.h>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>

// 定义控件ID
#define IDC_EDIT_FILENAME    1001
#define IDC_BUTTON_ANALYZE   1002
#define IDC_EDIT_ERRORS      1003
#define IDC_EDIT_RESULT      1004
#define IDC_STATIC_FILENAME  1005
#define IDC_STATIC_ERRORS    1006
#define IDC_STATIC_RESULT    1007

// 全局变量
HINSTANCE hInst;
HWND hMainWindow;
HWND hEditFilename, hButtonAnalyze, hEditErrors, hEditResult;

// 函数声明
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void PerformLexicalAnalysis();

// 主函数
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    hInst = hInstance;
    
    // 创建窗口类
    const wchar_t CLASS_NAME[] = L"LexicalAnalyzerWindowClass";
    
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.style = CS_HREDRAW | CS_VREDRAW;
    
    RegisterClass(&wc);
    
    // 创建主窗口
    hMainWindow = CreateWindowEx(
        0,
        CLASS_NAME,
        L"词法分析",
        WS_OVERLAPPEDWINDOW & ~WS_THICKFRAME & ~WS_MAXIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 500, 400,
        NULL,
        NULL,
        hInstance,
        NULL
    );
    
    if (hMainWindow == NULL) {
        return 0;
    }
    
    // 显示窗口
    ShowWindow(hMainWindow, nCmdShow);
    UpdateWindow(hMainWindow);
    
    // 确保窗口在最前端
    SetForegroundWindow(hMainWindow);
    SetFocus(hMainWindow);
    
    // 消息循环 - 确保程序持续运行直到用户关闭窗口
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    return (int)msg.wParam;
}

// 窗口过程函数
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_CREATE:
        // 创建静态文本 - 文件名
        CreateWindow(TEXT("STATIC"), TEXT("请输入分析的文件名:"),
            WS_CHILD | WS_VISIBLE | SS_LEFT,
            20, 20, 120, 20,
            hwnd, (HMENU)IDC_STATIC_FILENAME, hInst, NULL);
        
        // 创建文件名输入框
        hEditFilename = CreateWindow(TEXT("EDIT"), TEXT("")+"",
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            140, 20, 200, 20,
            hwnd, (HMENU)IDC_EDIT_FILENAME, hInst, NULL);
        
        // 创建分析按钮
        hButtonAnalyze = CreateWindow(TEXT("BUTTON"), TEXT("开始词法分析"),
            WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
            330, 18, 100, 24,
            hwnd, (HMENU)IDC_BUTTON_ANALYZE, hInst, NULL);
        
        // 创建静态文本 - 错误信息
        CreateWindow(TEXT("STATIC"), TEXT("输出的错误信息:"),
            WS_CHILD | WS_VISIBLE | SS_LEFT,
            20, 60, 120, 20,
            hwnd, (HMENU)IDC_STATIC_ERRORS, hInst, NULL);
        
        // 创建错误信息显示框
        hEditErrors = CreateWindow(TEXT("EDIT"), TEXT("")+"",
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_MULTILINE | WS_VSCROLL | ES_AUTOVSCROLL | ES_READONLY,
            20, 80, 450, 60,
            hwnd, (HMENU)IDC_EDIT_ERRORS, hInst, NULL);
        
        // 创建静态文本 - 输出结果
        CreateWindow(TEXT("STATIC"), TEXT("输出结果:"),
            WS_CHILD | WS_VISIBLE | SS_LEFT,
            20, 160, 120, 20,
            hwnd, (HMENU)IDC_STATIC_RESULT, hInst, NULL);
        
        // 创建结果显示框
        hEditResult = CreateWindow(TEXT("EDIT"), TEXT("")+"",
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_MULTILINE | WS_VSCROLL | ES_AUTOVSCROLL | ES_READONLY,
            20, 180, 450, 170,
            hwnd, (HMENU)IDC_EDIT_RESULT, hInst, NULL);
        
        return 0;
        
    case WM_COMMAND:
        switch (LOWORD(wParam)) {
        case IDC_BUTTON_ANALYZE:
            PerformLexicalAnalysis();
            return 0;
        }
        break;
        
    case WM_CLOSE:
        DestroyWindow(hwnd);
        return 0;
        
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

// 执行词法分析函数
void PerformLexicalAnalysis() {
    // 获取文件名
    TCHAR filename[256];
    GetWindowText(hEditFilename, filename, 256);
    
    // 清空错误信息和结果显示
    SetWindowText(hEditErrors, TEXT("")+"");
    SetWindowText(hEditResult, TEXT("")+"");
    
    // 检查文件名是否为空
    if (lstrlen(filename) == 0) {
        SetWindowText(hEditErrors, TEXT("请输入文件名"));
        // 聚焦到文件名输入框
        SetFocus(hEditFilename);
        return;
    }
    
    // 转换为std::string
    std::wstring wFilename(filename);
    std::string inputFile(wFilename.begin(), wFilename.end());
    
    Lexer lexer;
    
    // 加载源文件
    if (!lexer.loadFromFile(inputFile)) {
        // 更详细的错误信息
        std::wstring errorMsg = L"cannot open file: " + wFilename;
        SetWindowText(hEditErrors, errorMsg.c_str());
        return;
    }
    
    std::vector<Token> tokens;
    std::stringstream resultStream;
    
    try {
        // 词法分析
        while (lexer.hasMoreTokens()) {
            Token token = lexer.getNextToken();
            if (!token.value.empty()) {
                tokens.push_back(token);
                // 格式化为：值 类型 行号（使用表格形式显示）
                // 根据用户图片中的显示格式调整
                resultStream << std::left << std::setw(10) << token.value 
                             << std::setw(5) << token.type 
                             << std::setw(5) << token.line << "\r\n";
            }
        }
    } catch (const std::exception& e) {
        // 捕获可能的异常
        std::string errorStr = "Analysis error: " + std::string(e.what());
        std::wstring wError(errorStr.begin(), errorStr.end());
        SetWindowText(hEditErrors, wError.c_str());
        return;
    } catch (...) {
        // 捕获未知异常
        SetWindowText(hEditErrors, TEXT("发生未知错误"));
        return;
    }
    
    // 输出错误信息
    int errorCount = lexer.getErrorCount();
    
    // 将结果转换为TCHAR并显示
    std::string resultStr = resultStream.str();
    std::wstring wResult(resultStr.begin(), resultStr.end());
    SetWindowText(hEditResult, wResult.c_str());
    
    // 如果有错误，显示错误信息
    if (errorCount > 0) {
        std::stringstream errorStream;
        errorStream << "Error character count: " << errorCount;
        std::wstring wError(errorStream.str().begin(), errorStream.str().end());
        SetWindowText(hEditErrors, wError.c_str());
    } else {
        // 无错误时的提示
        if (tokens.empty()) {
            SetWindowText(hEditErrors, TEXT("文件中未发现可识别的token"));
        } else {
            std::stringstream successStream;
            successStream << "成功分析出 " << tokens.size() << " 个token";
            std::wstring wSuccess(successStream.str().begin(), successStream.str().end());
            SetWindowText(hEditErrors, wSuccess.c_str());
        }
    }
    
    // 确保窗口保持在前台，方便用户查看结果
    SetForegroundWindow(hMainWindow);
    SetFocus(hMainWindow);
    InvalidateRect(hMainWindow, NULL, TRUE);
    UpdateWindow(hMainWindow);
    
    // 为了解决闪退问题，我们在这里显示一个模式对话框，用户必须点击确定才能继续
    // 这是一个更强力的防止程序关闭的方法
    int result = MessageBox(hMainWindow, 
        L"词法分析已完成！\n\n点击确定继续使用程序，点击取消关闭程序。", 
        L"分析完成", 
        MB_OKCANCEL | MB_ICONINFORMATION | MB_SETFOREGROUND | MB_TOPMOST);
    
    // 如果用户点击取消，可以选择退出程序或执行其他操作
    if (result == IDCANCEL) {
        // 注意：这里不调用DestroyWindow或PostQuitMessage，让用户可以手动关闭窗口
        // 只是重新聚焦到主窗口，确保用户仍然可以交互
        SetForegroundWindow(hMainWindow);
        SetFocus(hMainWindow);
    }
}

