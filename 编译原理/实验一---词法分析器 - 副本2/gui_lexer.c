#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

// 全局变量定义
HWND hEditOutput, hButtonAnalyze, hEditFilename, hEditError;
HWND hLabelFilename, hLabelError, hLabelOutput;
HFONT hFont;
wchar_t inputBuffer[10000] = L"";
wchar_t outputBuffer[20000] = L"";

// 词法分析相关定义
typedef enum {
    KEYWORD, IDENTIFIER, NUMBER, OPERATOR, DELIMITER, UNKNOWN
} LexerTokenType;

// 关键字列表
const wchar_t *keywords[] = {L"main", L"int", L"float", L"double", L"char", L"if", L"else", L"for", L"while", L"return", L"void", L"printf"};
const int keywordCount = sizeof(keywords) / sizeof(keywords[0]);

// 函数声明
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);
void AnalyzeLexical(const wchar_t *input, wchar_t *output);
LexerTokenType CheckKeyword(const wchar_t *str);
LexerTokenType GetTokenType(const wchar_t *token);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const char CLASS_NAME[] = "LexerAnalyzerWindow";
    WNDCLASSEX wc;
    HWND hwnd;
    MSG Msg;
    RECT desktopRect;
    int windowWidth = 820;
    int windowHeight = 650;
    int posX, posY;

    // 创建支持中文的字体
    hFont = CreateFontW(16, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET,
                       OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY,
                       DEFAULT_PITCH | FF_SWISS, L"Microsoft YaHei");

    // 获取桌面分辨率以居中窗口
    GetWindowRect(GetDesktopWindow(), &desktopRect);
    posX = (desktopRect.right - windowWidth) / 2;
    posY = (desktopRect.bottom - windowHeight) / 2;

    // 注册窗口类
    wc.cbSize        = sizeof(WNDCLASSEX);
    wc.style         = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc   = WndProc;
    wc.cbClsExtra    = 0;
    wc.cbWndExtra    = 0;
    wc.hInstance     = hInstance;
    wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszMenuName  = NULL;
    wc.lpszClassName = CLASS_NAME;
    wc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);

    if(!RegisterClassEx(&wc)) {
        MessageBoxW(NULL, L"窗口类注册失败！", L"错误", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    // 创建窗口
    hwnd = CreateWindowExA(
        0,
        CLASS_NAME,
        "词法分析器",
        WS_OVERLAPPEDWINDOW,
        posX, posY, windowWidth, windowHeight,
        NULL, NULL, hInstance, NULL);

    if(hwnd == NULL) {
        MessageBoxW(NULL, L"窗口创建失败！", L"错误", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    // 确保窗口可见并获得焦点
    ShowWindow(hwnd, SW_SHOWDEFAULT);
    UpdateWindow(hwnd);
    SetForegroundWindow(hwnd);
    SetFocus(hwnd);

    // 消息循环
    while(GetMessage(&Msg, NULL, 0, 0) > 0) {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }

    DeleteObject(hFont);
    return Msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch(msg) {
        case WM_CREATE:
            // 创建文件名标签
            hLabelFilename = CreateWindowExW(
                0,
                L"STATIC",
                L"请输入分析的文件名:",
                WS_CHILD | WS_VISIBLE | SS_LEFT,
                20, 20, 200, 25,
                hwnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
            SendMessageW(hLabelFilename, WM_SETFONT, (WPARAM)hFont, TRUE);
            
            // 创建文件名输入框
            hEditFilename = CreateWindowExW(
                WS_EX_CLIENTEDGE,
                L"EDIT",
                L"program.txt",
                WS_CHILD | WS_VISIBLE | ES_AUTOHSCROLL,
                20, 50, 300, 25,
                hwnd, (HMENU)1, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
            SendMessageW(hEditFilename, WM_SETFONT, (WPARAM)hFont, TRUE);
            

            
            // 创建分析按钮
            hButtonAnalyze = CreateWindowExW(
                0,
                L"BUTTON",
                L"开始词法分析",
                WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                320, 90, 160, 40,
                hwnd, (HMENU)3, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
            SendMessageW(hButtonAnalyze, WM_SETFONT, (WPARAM)hFont, TRUE);
            
            // 创建错误信息显示标签
            hLabelError = CreateWindowExW(
                0,
                L"STATIC",
                L"错误信息:",
                WS_CHILD | WS_VISIBLE | SS_LEFT,
                20, 150, 200, 25,
                hwnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
            SendMessageW(hLabelError, WM_SETFONT, (WPARAM)hFont, TRUE);
            
            // 创建错误信息文本框
            hEditError = CreateWindowExW(
                WS_EX_CLIENTEDGE,
                L"EDIT",
                L"",
                WS_CHILD | WS_VISIBLE | WS_VSCROLL | WS_HSCROLL | ES_MULTILINE | ES_AUTOVSCROLL | ES_AUTOHSCROLL | ES_READONLY,
                20, 180, 760, 80,
                hwnd, (HMENU)4, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
            SendMessageW(hEditError, WM_SETFONT, (WPARAM)hFont, TRUE);
            
            // 创建结果输出标签
            hLabelOutput = CreateWindowExW(
                0,
                L"STATIC",
                L"词法分析结果:",
                WS_CHILD | WS_VISIBLE | SS_LEFT,
                20, 280, 200, 25,
                hwnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
            SendMessageW(hLabelOutput, WM_SETFONT, (WPARAM)hFont, TRUE);
            
            // 创建结果输出文本框
            hEditOutput = CreateWindowExW(
                WS_EX_CLIENTEDGE,
                L"EDIT",
                L"",
                WS_CHILD | WS_VISIBLE | WS_VSCROLL | WS_HSCROLL | ES_MULTILINE | ES_AUTOVSCROLL | ES_AUTOHSCROLL | ES_READONLY,
                20, 310, 760, 300,
                hwnd, (HMENU)5, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
            SendMessageW(hEditOutput, WM_SETFONT, (WPARAM)hFont, TRUE);
            
            break;
            
        case WM_COMMAND:
            if (LOWORD(wParam) == 3 && HIWORD(wParam) == BN_CLICKED) { // 分析按钮被点击
                wchar_t filename[256];
                wchar_t fileContent[10000] = L"";
                
                // 获取文件名
                GetWindowTextW(hEditFilename, filename, sizeof(filename)/sizeof(wchar_t));
                
                // 尝试从文件读取内容
                FILE *file = _wfopen(filename, L"r, ccs=UTF-8");
                if (file) {
                    wchar_t line[1024];
                    while (fgetws(line, sizeof(line)/sizeof(wchar_t), file)) {
                        wcscat_s(fileContent, sizeof(fileContent)/sizeof(wchar_t), line);
                    }
                    fclose(file);
                    
                    // 显示成功消息
                    SetWindowTextW(hEditError, L"文件读取成功！");
                    
                    // 执行词法分析
                    AnalyzeLexical(fileContent, outputBuffer);
                    
                    // 显示分析结果
                    SetWindowTextW(hEditOutput, outputBuffer);
                    
                    // 显示成功消息
                    MessageBoxW(hwnd, L"词法分析完成！", L"提示", MB_ICONINFORMATION | MB_OK);
                } else {
                    SetWindowTextW(hEditError, L"文件读取失败！请检查文件名是否正确。");
                    SetWindowTextW(hEditOutput, L"");
                }
            }
            break;
            
        case WM_SIZE:
            // 窗口大小改变时调整控件位置
            if (hEditOutput && hButtonAnalyze && hEditFilename && hEditError && 
                hLabelFilename && hLabelError && hLabelOutput) {
                int clientWidth = LOWORD(lParam);
                int clientHeight = HIWORD(lParam);
                
                // 调整标签位置
                MoveWindow(hLabelFilename, 20, 20, 200, 25, TRUE);
                MoveWindow(hLabelError, 20, 150, 200, 25, TRUE);
                MoveWindow(hLabelOutput, 20, 280, 200, 25, TRUE);
                
                // 调整输入框位置
                MoveWindow(hEditFilename, 20, 50, clientWidth - 40, 25, TRUE);
                MoveWindow(hEditError, 20, 180, clientWidth - 40, 80, TRUE);
                MoveWindow(hEditOutput, 20, 310, clientWidth - 40, clientHeight - 330, TRUE);
                
                // 调整按钮位置
                MoveWindow(hButtonAnalyze, (clientWidth - 160) / 2, 90, 160, 40, TRUE);
            }
            break;
            
        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;
            
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
            
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

// 词法分析函数
void AnalyzeLexical(const wchar_t *input, wchar_t *output) {
    wchar_t *token;          // 当前分析的标记
    wchar_t *inputCopy;      // 输入字符串的副本
    wchar_t *saveptr = NULL;
    wchar_t *line;           // 当前行
    int lineNum = 1;
    int errorCount = 0;
    wchar_t errorMessages[1000] = L"";
    
    // 创建输入的副本以便安全地进行字符串操作
    inputCopy = wcsdup(input);
    if (!inputCopy) {
        swprintf(output, 20000, L"内存分配失败！");
        return;
    }
    
    // 初始化输出缓冲区
    swprintf(output, 20000, L"词法分析结果\n");
    swprintf(output + wcslen(output), 20000 - wcslen(output), L"====================================\n");
    
    // 逐行分析 - 使用更安全的方法分割行
    wchar_t *lineStart = inputCopy;
    wchar_t *lineEnd;
    
    while (lineStart && *lineStart) {
        // 找到行结束位置
        lineEnd = wcschr(lineStart, L'\n');
        if (!lineEnd) {
            lineEnd = lineStart + wcslen(lineStart);
        }
        
        // 创建当前行的副本
        size_t lineLength = lineEnd - lineStart;
        wchar_t *lineCopy = (wchar_t*)malloc((lineLength + 1) * sizeof(wchar_t));
        if (!lineCopy) {
            swprintf(output + wcslen(output), 20000 - wcslen(output), L"内存分配失败！");
            free(inputCopy);
            return;
        }
        wcsncpy(lineCopy, lineStart, lineLength);
        lineCopy[lineLength] = L'\0';
        
        // 移除行尾的回车符
        if (lineLength > 0 && lineCopy[lineLength-1] == L'\r') {
            lineCopy[lineLength-1] = L'\0';
        }
        
        // 跳过空行
        if (wcslen(lineCopy) == 0) {
            free(lineCopy);
            if (*lineEnd == L'\n') {
                lineStart = lineEnd + 1;
            } else {
                lineStart = NULL;
            }
            lineNum++;
            continue;
        }
        
        // 检查是否是预处理指令（以#开头）
        if (lineCopy[0] == L'#') {
            // 预处理指令作为整体处理
            swprintf(output + wcslen(output), 20000 - wcslen(output), L"第%d行 标记: %ls\n", lineNum, lineCopy);
            swprintf(output + wcslen(output), 20000 - wcslen(output), L"  类型: 预处理指令\n");
            swprintf(output + wcslen(output), 20000 - wcslen(output), L"  --------------------\n");
            free(lineCopy);
            if (*lineEnd == L'\n') {
                lineStart = lineEnd + 1;
            } else {
                lineStart = NULL;
            }
            lineNum++;
            continue;
        }
        
        // 解析行中的标记
        wchar_t *token = wcstok(lineCopy, L" \t(){}[];,=+-*/<>!&|\"'");
        while (token != NULL) {
            // 跳过空标记
            if (wcslen(token) == 0) {
                token = wcstok(NULL, L" \t(){}[];,=+-*/<>!&|\"'");
                continue;
            }
            
            // 检查标记类型
            LexerTokenType type = GetTokenType(token);
            
            // 输出标记信息
            const wchar_t *typeStr;
            switch (type) {
                case KEYWORD:   typeStr = L"关键字";
                               break;
                case IDENTIFIER: typeStr = L"标识符";
                               break;
                case NUMBER:    typeStr = L"数字";
                               break;
                case OPERATOR:  typeStr = L"运算符";
                               break;
                case DELIMITER: typeStr = L"分界符";
                               break;
                case UNKNOWN:   typeStr = L"未知字符";
                               break;
                default:        typeStr = L"未知";
            }
            
            // 竖向展示：每个标记单独一行显示详细信息
            swprintf(output + wcslen(output), 20000 - wcslen(output), L"第%d行 标记: %ls\n", lineNum, token);
            swprintf(output + wcslen(output), 20000 - wcslen(output), L"  类型: %ls\n", typeStr);
            swprintf(output + wcslen(output), 20000 - wcslen(output), L"  --------------------\n");
            
            // 移到下一个标记
            token = wcstok(NULL, L" \t(){}[];,=+-*/<>!&|\"'");
        }
        
        // 检查行中的特殊字符和运算符（避免重复输出）
        wchar_t *pos = lineStart;
        int inString = 0;  // 是否在字符串内
        int inChar = 0;    // 是否在字符内
        
        while (pos < lineEnd) {
            if (*pos == L'\"' && !inChar) {
                inString = !inString;  // 切换字符串状态
            } else if (*pos == L'\'' && !inString) {
                inChar = !inChar;      // 切换字符状态
            }
            
            // 不在字符串或字符内时检查特殊字符
            if (!inString && !inChar && wcschr(L"(){}[];,=+-*/<>!&|", *pos)) {
                wchar_t special[2] = {*pos, L'\0'};
                LexerTokenType type = GetTokenType(special);
                const wchar_t *typeStr;
                
                switch (type) {
                    case OPERATOR:  typeStr = L"运算符";
                                   break;
                    case DELIMITER: typeStr = L"分界符";
                                   break;
                    default:        typeStr = L"未知字符";
                }
                
                // 竖向展示特殊字符
                swprintf(output + wcslen(output), 20000 - wcslen(output), L"第%d行 标记: %lc\n", lineNum, *pos);
                swprintf(output + wcslen(output), 20000 - wcslen(output), L"  类型: %ls\n", typeStr);
                swprintf(output + wcslen(output), 20000 - wcslen(output), L"  --------------------\n");
            }
            
            // 处理字符串和字符内容
            if (inString || inChar) {
                // 字符串或字符内容作为整体处理
                wchar_t *strStart = pos;
                wchar_t *strEnd = pos;
                while (strEnd < lineEnd && ((inString && *strEnd != L'\"') || (inChar && *strEnd != L'\''))) {
                    strEnd++;
                }
                
                if (strEnd < lineEnd) {
                    size_t strLength = strEnd - strStart;
                    if (strLength > 0) {
                        wchar_t *strContent = (wchar_t*)malloc((strLength + 1) * sizeof(wchar_t));
                        wcsncpy(strContent, strStart, strLength);
                        strContent[strLength] = L'\0';
                        
                        swprintf(output + wcslen(output), 20000 - wcslen(output), L"第%d行 标记: %ls\n", lineNum, strContent);
                        swprintf(output + wcslen(output), 20000 - wcslen(output), L"  类型: %ls\n", inString ? L"字符串字面量" : L"字符字面量");
                        swprintf(output + wcslen(output), 20000 - wcslen(output), L"  --------------------\n");
                        
                        free(strContent);
                        pos = strEnd; // 跳过已处理的字符串/字符内容
                    }
                }
            }
            
            pos++;
        }
        
        free(lineCopy);
        
        // 移动到下一行
        if (*lineEnd == L'\n') {
            lineStart = lineEnd + 1;
        } else {
            lineStart = NULL;
        }
        lineNum++;
    }
    
    // 输出错误信息和总结
    swprintf(output + wcslen(output), 20000 - wcslen(output), L"====================================\n");
    if (errorCount > 0) {
        swprintf(output + wcslen(output), 20000 - wcslen(output), L"总计: %d 个错误\n", errorCount);
        swprintf(output + wcslen(output), 20000 - wcslen(output), L"错误详情: %ls\n", errorMessages);
    } else {
        swprintf(output + wcslen(output), 20000 - wcslen(output), L"无错误\n");
    }
    swprintf(output + wcslen(output), 20000 - wcslen(output), L"分析完成！");
    
    free(inputCopy);
}

// 检查字符串是否为关键字
LexerTokenType CheckKeyword(const wchar_t *str) {
    for (int i = 0; i < keywordCount; i++) {
        if (wcscmp(str, keywords[i]) == 0) {
            return KEYWORD;
        }
    }
    return IDENTIFIER;
}

// 获取标记类型
LexerTokenType GetTokenType(const wchar_t *token) {
    // 检查是否为关键字
    if (CheckKeyword(token) == KEYWORD) {
        return KEYWORD;
    }
    
    // 检查是否为标识符（字母或下划线开头）
    if ((iswalpha(token[0]) || token[0] == L'_') && wcslen(token) > 0) {
        int i = 1;
        while (token[i] && (iswalnum(token[i]) || token[i] == L'_')) {
            i++;
        }
        if (token[i] == L'\0') {
            return IDENTIFIER;
        }
    }
    
    // 检查是否为数字
    if ((iswdigit(token[0]) || token[0] == L'.') && wcslen(token) > 0) {
        int dotCount = 0;
        int i = (token[0] == L'.') ? 1 : 0;
        dotCount = (token[0] == L'.') ? 1 : 0;
        
        while (token[i]) {
            if (token[i] == L'.') {
                dotCount++;
                if (dotCount > 1) break;
            } else if (!iswdigit(token[i])) {
                break;
            }
            i++;
        }
        
        if (token[i] == L'\0' && (dotCount <= 1)) {
            // 确保不是单独的点号
            if (wcslen(token) > 1 || (wcslen(token) == 1 && iswdigit(token[0]))) {
                return NUMBER;
            }
        }
    }
    
    // 检查是否为运算符
    if (wcschr(L"=+-*/<>!&|~", token[0]) && wcslen(token) == 1) {
        return OPERATOR;
    }
    
    // 检查是否为分界符
    if (wcschr(L"(){}[];,\"'", token[0]) && wcslen(token) == 1) {
        return DELIMITER;
    }
    
    // 未知字符
    return UNKNOWN;
}