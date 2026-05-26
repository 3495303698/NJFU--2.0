#include "lexer.h"
#include <windows.h>
#include <commdlg.h>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <fstream>

// 定义控件ID
#define IDC_EDIT_FILENAME    1001
#define IDC_BUTTON_BROWSE    1002
#define IDC_BUTTON_ANALYZE   1003
#define IDC_BUTTON_SAVE      1004
#define IDC_EDIT_ERRORS      1005
#define IDC_EDIT_RESULT      1006
#define IDC_STATIC_FILENAME  1007
#define IDC_STATIC_ERRORS    1008
#define IDC_STATIC_RESULT    1009

// 全局变量
HINSTANCE hInst;
HWND hMainWindow;
HWND hEditFilename, hButtonBrowse, hButtonAnalyze, hButtonSave, hEditErrors, hEditResult;
std::string lastResult;  // 保存最后一次分析结果

// 函数声明
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void PerformLexicalAnalysis();
void BrowseForFile();
void SaveResult();
std::wstring StringToWString(const std::string& str);
std::string WStringToString(const std::wstring& wstr);

// 主函数
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    hInst = hInstance;
    
    // 创建窗口类
    const char CLASS_NAME[] = "LexicalAnalyzerWindowClass";
    
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.style = CS_HREDRAW | CS_VREDRAW;
    
    RegisterClass(&wc);
    
    // 创建主窗口 - 增大窗口尺寸以容纳更多内容
    hMainWindow = CreateWindowEx(
        0,
        CLASS_NAME,
        "词法分析器 - 编译原理实验一"
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
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
        CreateWindow(TEXT("STATIC"), TEXT("源文件路径:"),
            WS_CHILD | WS_VISIBLE | SS_LEFT,
            20, 20, 100, 25,
            hwnd, (HMENU)IDC_STATIC_FILENAME, hInst, NULL);
        
        // 创建文件名输入框
        hEditFilename = CreateWindow(TEXT("EDIT"), TEXT(""),
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_AUTOHSCROLL,
            20, 45, 500, 25,
            hwnd, (HMENU)IDC_EDIT_FILENAME, hInst, NULL);
        
        // 创建浏览按钮
        hButtonBrowse = CreateWindow(TEXT("BUTTON"), TEXT("浏览..."),
            WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
            530, 43, 80, 28,
            hwnd, (HMENU)IDC_BUTTON_BROWSE, hInst, NULL);
        
        // 创建分析按钮
        hButtonAnalyze = CreateWindow(TEXT("BUTTON"), TEXT("开始词法分析"),
            WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON | BS_DEFPUSHBUTTON,
            620, 43, 120, 28,
            hwnd, (HMENU)IDC_BUTTON_ANALYZE, hInst, NULL);
        
        // 创建静态文本 - 错误信息
        CreateWindow(TEXT("STATIC"), TEXT("分析状态信息:"),
            WS_CHILD | WS_VISIBLE | SS_LEFT,
            20, 85, 120, 25,
            hwnd, (HMENU)IDC_STATIC_ERRORS, hInst, NULL);
        
        // 创建错误信息显示框
        hEditErrors = CreateWindow(TEXT("EDIT"), TEXT(""),
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_MULTILINE | WS_VSCROLL | ES_AUTOVSCROLL | ES_READONLY,
            20, 110, 720, 60,
            hwnd, (HMENU)IDC_EDIT_ERRORS, hInst, NULL);
        
        // 创建静态文本 - 输出结果
        CreateWindow(TEXT("STATIC"), TEXT("词法分析结果 (格式: 单词值 | 类型 | 行号):"),
            WS_CHILD | WS_VISIBLE | SS_LEFT,
            20, 185, 300, 25,
            hwnd, (HMENU)IDC_STATIC_RESULT, hInst, NULL);
        
        // 创建保存按钮
        hButtonSave = CreateWindow(TEXT("BUTTON"), TEXT("保存结果"),
            WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
            620, 183, 120, 28,
            hwnd, (HMENU)IDC_BUTTON_SAVE, hInst, NULL);
        
        // 创建结果显示框
        hEditResult = CreateWindow(TEXT("EDIT"), TEXT(""),
            WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_MULTILINE | WS_VSCROLL | ES_AUTOVSCROLL | ES_READONLY,
            20, 220, 720, 320,
            hwnd, (HMENU)IDC_EDIT_RESULT, hInst, NULL);
        
        // 设置字体为等宽字体，便于对齐显示
        HFONT hFont = CreateFont(
            14, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
            DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
            DEFAULT_QUALITY, FIXED_PITCH | FF_MODERN, TEXT("Consolas")
        );
        SendMessage(hEditResult, WM_SETFONT, (WPARAM)hFont, TRUE);
        
        return 0;
        
    case WM_COMMAND:
        switch (LOWORD(wParam)) {
        case IDC_BUTTON_BROWSE:
            BrowseForFile();
            return 0;
        case IDC_BUTTON_ANALYZE:
            PerformLexicalAnalysis();
            return 0;
        case IDC_BUTTON_SAVE:
            SaveResult();
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

// 字符串转换辅助函数
// 使用系统默认代码页(CP_ACP)以正确处理中文字符
std::wstring StringToWString(const std::string& str) {
    if (str.empty()) return std::wstring();
    int size_needed = MultiByteToWideChar(CP_ACP, 0, &str[0], (int)str.size(), NULL, 0);
    std::wstring wstrTo(size_needed, 0);
    MultiByteToWideChar(CP_ACP, 0, &str[0], (int)str.size(), &wstrTo[0], size_needed);
    return wstrTo;
}

std::string WStringToString(const std::wstring& wstr) {
    if (wstr.empty()) return std::string();
    int size_needed = WideCharToMultiByte(CP_ACP, 0, &wstr[0], (int)wstr.size(), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_ACP, 0, &wstr[0], (int)wstr.size(), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

// 浏览文件函数
void BrowseForFile() {
    OPENFILENAME ofn;
    TCHAR szFile[512] = {0};  // 增大缓冲区以支持长路径
    
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(OPENFILENAME);
    ofn.hwndOwner = hMainWindow;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile) / sizeof(TCHAR);
    ofn.lpstrFilter = TEXT("文本文件\0*.txt\0C源文件\0*.c\0所有文件\0*.*\0");
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST | OFN_EXPLORER;
    
    if (GetOpenFileName(&ofn) == TRUE) {
        SetWindowText(hEditFilename, szFile);
    }
}

// 保存结果函数
void SaveResult() {
    if (lastResult.empty()) {
        MessageBox(hMainWindow, L"没有可保存的结果！\n请先进行词法分析。", L"提示", MB_OK | MB_ICONINFORMATION);
        return;
    }
    
    OPENFILENAME ofn;
    TCHAR szFile[512] = {0};  // 增大缓冲区以支持长路径
    lstrcpy(szFile, TEXT("output.txt"));
    
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(OPENFILENAME);
    ofn.hwndOwner = hMainWindow;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile) / sizeof(TCHAR);
    ofn.lpstrFilter = TEXT("文本文件\0*.txt\0所有文件\0*.*\0");
    ofn.nFilterIndex = 1;
    ofn.lpstrDefExt = TEXT("txt");
    ofn.Flags = OFN_OVERWRITEPROMPT | OFN_EXPLORER;
    
    if (GetSaveFileName(&ofn) == TRUE) {
        std::string filename = WStringToString(szFile);
        std::ofstream outFile(filename, std::ios::out | std::ios::trunc);
        if (outFile.is_open()) {
            outFile << lastResult;
            outFile.close();
            MessageBox(hMainWindow, L"结果已成功保存！", L"保存成功", MB_OK | MB_ICONINFORMATION);
        } else {
            MessageBox(hMainWindow, L"无法保存文件！\n请检查文件路径和权限。", L"错误", MB_OK | MB_ICONERROR);
        }
    }
}

// 执行词法分析函数
void PerformLexicalAnalysis() {
    // 获取文件名
    TCHAR filename[512];
    GetWindowText(hEditFilename, filename, 512);
    
    // 清空错误信息和结果显示
    SetWindowText(hEditErrors, TEXT(""));
    SetWindowText(hEditResult, TEXT(""));
    lastResult.clear();
    
    // 检查文件名是否为空
    if (lstrlen(filename) == 0) {
        SetWindowText(hEditErrors, TEXT("错误: 请选择或输入源文件路径"));
        SetFocus(hEditFilename);
        return;
    }
    
    // 转换为std::string
    std::string inputFile = WStringToString(filename);
    
    Lexer lexer;
    
    // 加载源文件
    if (!lexer.loadFromFile(inputFile)) {
        std::wstring errorMsg = L"错误: 无法打开文件\n" + std::wstring(filename);
        SetWindowText(hEditErrors, errorMsg.c_str());
        return;
    }
    
    std::vector<Token> tokens;
    std::stringstream resultStream;
    
    // 添加表头
    resultStream << std::left << std::setw(25) << "单词值" 
                 << std::setw(15) << "类型" 
                 << std::setw(10) << "行号" << "\r\n";
    resultStream << std::string(50, '-') << "\r\n";
    
    try {
        // 词法分析
        while (lexer.hasMoreTokens()) {
            Token token = lexer.getNextToken();
            if (!token.value.empty()) {
                tokens.push_back(token);
                
                // 获取类型名称
                std::string typeName;
                switch (token.type) {
                    case TOKEN_KEYWORD: typeName = "保留字(1)"; break;
                    case TOKEN_IDENTIFIER: typeName = "标识符(2)"; break;
                    case TOKEN_CONSTANT: typeName = "常数(3)"; break;
                    case TOKEN_OPERATOR: typeName = "运算符(4)"; break;
                    case TOKEN_DELIMITER: typeName = "分隔符(5)"; break;
                    default: typeName = "未知"; break;
                }
                
                // 格式化为表格形式显示
                resultStream << std::left << std::setw(25) << token.value 
                             << std::setw(15) << typeName
                             << std::setw(10) << token.line << "\r\n";
            }
        }
    } catch (const std::exception& e) {
        std::string errorStr = "分析错误: " + std::string(e.what());
        SetWindowText(hEditErrors, StringToWString(errorStr).c_str());
        return;
    } catch (...) {
        SetWindowText(hEditErrors, TEXT("发生未知错误"));
        return;
    }
    
    // 保存结果字符串
    lastResult = resultStream.str();
    
    // 将结果转换为宽字符串并显示
    SetWindowText(hEditResult, StringToWString(lastResult).c_str());
    
    // 显示分析状态信息
    int errorCount = lexer.getErrorCount();
    std::stringstream statusStream;
    
    if (errorCount > 0) {
        statusStream << "分析完成！发现 " << errorCount << " 个错误字符。";
    } else {
        if (tokens.empty()) {
            statusStream << "分析完成！文件中未发现可识别的token。";
        } else {
            statusStream << "分析完成！成功识别出 " << tokens.size() << " 个token，无错误。";
        }
    }
    
    SetWindowText(hEditErrors, StringToWString(statusStream.str()).c_str());
    
    // 刷新窗口
    InvalidateRect(hMainWindow, NULL, TRUE);
    UpdateWindow(hMainWindow);
}

