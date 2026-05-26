// 示例程序：演示如何使用 Parser 类
// 这是一个简单的示例，展示如何在自己的程序中使用递归下降分析器

#include <iostream>
#include "../include/parser.h"

using namespace std;

int main() {
    // 测试用例数组
    string testCases[] = {
        "i+i#",      // 合法
        "i-i#",      // 合法
        "i*i#",      // 合法
        "i/i#",      // 合法
        "i+i*i#",    // 合法
        "(i+i)*i#",  // 合法
        "i+i*#",     // 非法
        "i++#",      // 非法
        "(i+i#",     // 非法
    };
    
    cout << "========== 递归下降分析程序测试 ==========" << endl;
    cout << endl;
    
    for (int i = 0; i < 9; i++) {
        cout << "测试用例 " << (i + 1) << ": " << testCases[i] << endl;
        
        Parser parser(testCases[i]);
        bool result = parser.parse();
        
        if (result) {
            cout << "结果: 合法符号串" << endl;
        } else {
            cout << "结果: 非法符号串" << endl;
            cout << "错误: " << parser.getError() << endl;
        }
        
        cout << "----------------------------------------" << endl;
    }
    
    return 0;
}
