#ifndef LEXER_H
#define LEXER_H

#include <string>
#include <vector>
#include <fstream>
#include <map>

// Token类型定义
enum TokenType {
    TOKEN_KEYWORD = 1,      // 保留字
    TOKEN_IDENTIFIER = 2,   // 标识符
    TOKEN_CONSTANT = 3,     // 常数
    TOKEN_OPERATOR = 4,     // 运算符
    TOKEN_DELIMITER = 5    // 分隔符
};

// Token结构
struct Token {
    TokenType type;
    std::string value;
    int line;  // 行号
    
    Token(TokenType t, const std::string& v, int l) : type(t), value(v), line(l) {}
};

// 词法分析器类
class Lexer {
private:
    std::string source;          // 源程序字符串
    size_t pos;                  // 当前位置
    int line;                    // 当前行号
    int errorCount;              // 错误计数
    
    // 保留字表
    std::map<std::string, bool> keywords;
    
    // 初始化保留字表
    void initKeywords();
    
    // 跳过空白字符
    void skipWhitespace();
    
    // 判断是否为字母
    bool isLetter(char c);
    
    // 判断是否为数字
    bool isDigit(char c);
    
    // 判断是否为空白字符
    bool isWhitespace(char c);
    
    // 获取当前字符
    char currentChar();
    
    // 获取下一个字符
    char nextChar();
    
    // 回退一个字符
    void backChar();
    
    // 识别标识符或保留字
    Token scanIdentifierOrKeyword();
    
    // 识别数字
    Token scanNumber();
    
    // 识别字符串常量
    Token scanString();
    
    // 识别运算符
    Token scanOperator();
    
    // 识别分隔符
    Token scanDelimiter();
    
public:
    Lexer();
    
    // 从文件加载源程序
    bool loadFromFile(const std::string& filename);
    
    // 从字符串加载源程序
    void loadFromString(const std::string& code);
    
    // 获取下一个Token
    Token getNextToken();
    
    // 判断是否还有更多Token
    bool hasMoreTokens();
    
    // 获取错误计数
    int getErrorCount() const;
    
    // 重置分析器
    void reset();
};

#endif // LEXER_H

