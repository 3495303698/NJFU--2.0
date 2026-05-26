#include "lexer.h"
#include <iostream>
#include <string>
#include <fstream>

void printToken(const Token& token, std::ostream& out) {
    std::string typeStr;
    switch (token.type) {
        case TOKEN_KEYWORD:
            typeStr = "关键字";
            break;
        case TOKEN_IDENTIFIER:
            typeStr = "标识符";
            break;
        case TOKEN_CONSTANT:
            typeStr = "常数";
            break;
        case TOKEN_OPERATOR:
            typeStr = "运算符";
            break;
        case TOKEN_DELIMITER:
            typeStr = "分隔符";
            break;
        default:
            typeStr = "未知";
    }
    out << "(" << token.type << ", \"" << token.value << "\")" << std::endl;
}

int main(int argc, char* argv[]) {
    Lexer lexer;
    std::string filename;
    std::string outputFilename = "output.txt";
    
    // 处理命令行参数
    if (argc >= 2) {
        filename = argv[1];
        if (argc >= 3) {
            outputFilename = argv[2];
        }
    } else {
        // 交互式输入
        std::cout << "请输入要分析的文件名: ";
        std::cin >> filename;
    }
    
    // 加载文件
    if (!lexer.loadFromFile(filename)) {
        std::cerr << "无法打开文件: " << filename << std::endl;
        std::cout << "按回车键退出...";
        std::cin.get();
        std::cin.get();
        return 1;
    }
    
    // 创建输出文件
    std::ofstream outFile(outputFilename);
    if (!outFile.is_open()) {
        std::cerr << "无法创建输出文件: " << outputFilename << std::endl;
        std::cout << "按回车键退出...";
        std::cin.get();
        std::cin.get();
        return 1;
    }
    
    // 进行词法分析
    std::cout << "开始词法分析..." << std::endl;
    std::cout << "分析结果将保存到: " << outputFilename << std::endl;
    std::cout << "----------------------------------------" << std::endl;
    
    while (lexer.hasMoreTokens()) {
        Token token = lexer.getNextToken();
        printToken(token, std::cout);
        printToken(token, outFile);
    }
    
    std::cout << "----------------------------------------" << std::endl;
    std::cout << "词法分析完成!" << std::endl;
    std::cout << "错误字符数: " << lexer.getErrorCount() << std::endl;
    
    outFile.close();
    
    // 等待用户按键再退出
    std::cout << "按回车键退出...";
    std::cin.get();
    std::cin.get();
    
    return 0;
}