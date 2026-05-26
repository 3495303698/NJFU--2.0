#include <iostream>
#include <string>
#include "../include/parser.h"
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>

using namespace std;

void printHeader() {
    cout << "----------递归下降分析程序,编制人:张三,2023001,计算机1班" << endl;
}

void printPrompt() {
    cout << "输入一以#结束的符号串(包括+-*/()i#): ";
}

int main() {
    // 设置控制台代码页为 UTF-8 以支持中文输出
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    
    string input;
    
    printHeader();
    printPrompt();
    
    getline(cin, input);
    
    // 创建分析器并执行分析
    Parser parser(input);
    bool result = parser.parse();
    
    // 输出结果
    if (result) {
        cout << input << "为合法符号串!" << endl;
    } else {
        cout << input << "为非法符号串!" << endl;
        cout << "错误信息: " << parser.getError() << endl;
    }
    
    cout << "请按任意键继续..." << endl;
    cin.get();  // 等待用户按键
    
    return 0;
}
