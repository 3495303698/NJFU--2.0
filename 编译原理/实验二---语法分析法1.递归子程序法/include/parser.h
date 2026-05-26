#ifndef PARSER_H
#define PARSER_H

#include <string>
#include <iostream>

// 词法单元类型
enum TokenType {
    TOKEN_PLUS,      // +
    TOKEN_MINUS,     // -
    TOKEN_MULTIPLY,  // *
    TOKEN_DIVIDE,    // /
    TOKEN_LPAREN,    // (
    TOKEN_RPAREN,    // )
    TOKEN_IDENTIFIER, // i
    TOKEN_END,       // #
    TOKEN_ERROR      // 错误
};

class Parser {
private:
    std::string input;        // 输入字符串
    size_t pos;               // 当前位置
    TokenType currentToken;   // 当前词法单元
    bool hasError;            // 是否有错误
    std::string errorMsg;     // 错误信息

    // 词法分析：获取下一个词法单元
    void nextToken();
    
    // 语法分析函数（对应文法中的每个非终结符）
    void E();  // E -> TG
    void G();  // G -> +TG | -TG | ε
    void T();  // T -> FS
    void S();  // S -> *FS | /FS | ε
    void F();  // F -> (E) | i

    // 错误处理
    void error(const std::string& msg);

public:
    Parser(const std::string& inputStr);
    
    // 执行语法分析
    bool parse();
    
    // 获取错误信息
    std::string getError() const { return errorMsg; }
    
    // 检查是否成功
    bool isSuccess() const { return !hasError; }
};

#endif // PARSER_H
