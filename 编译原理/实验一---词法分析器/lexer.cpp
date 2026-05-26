#include "lexer.h"
#include <cctype>
#include <iostream>

Lexer::Lexer() : pos(0), line(1), errorCount(0) {
    initKeywords();
}

void Lexer::initKeywords() {
    keywords["main"] = true;
    keywords["printf"] = true;
    keywords["if"] = true;
    keywords["int"] = true;
    keywords["for"] = true;
    keywords["while"] = true;
    keywords["do"] = true;
    keywords["return"] = true;
    keywords["break"] = true;
    keywords["continue"] = true;
}

bool Lexer::loadFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        return false;
    }
    
    source.clear();
    std::string line;
    while (std::getline(file, line)) {
        source += line + "\n";
    }
    file.close();
    
    reset();
    return true;
}

void Lexer::loadFromString(const std::string& code) {
    source = code;
    reset();
}

void Lexer::reset() {
    pos = 0;
    line = 1;
    errorCount = 0;
}

char Lexer::currentChar() {
    if (pos >= source.length()) {
        return '\0';
    }
    return source[pos];
}

char Lexer::nextChar() {
    if (pos >= source.length()) {
        return '\0';
    }
    char c = source[pos++];
    if (c == '\n') {
        line++;
    }
    return c;
}

void Lexer::backChar() {
    if (pos > 0) {
        pos--;
        if (source[pos] == '\n') {
            line--;
        }
    }
}

bool Lexer::isLetter(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}

bool Lexer::isDigit(char c) {
    return c >= '0' && c <= '9';
}

bool Lexer::isWhitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

void Lexer::skipWhitespace() {
    while (pos < source.length() && isWhitespace(source[pos])) {
        if (source[pos] == '\n') {
            line++;
        }
        pos++;
    }
}

Token Lexer::scanIdentifierOrKeyword() {
    std::string value;
    int startLine = line;
    
    while (pos < source.length()) {
        char c = currentChar();
        if (isLetter(c) || isDigit(c)) {
            value += c;
            nextChar();
        } else {
            break;
        }
    }
    
    // 检查是否为保留字
    if (keywords.find(value) != keywords.end()) {
        return Token(TOKEN_KEYWORD, value, startLine);
    } else {
        // 标识符前20个字符有效
        if (value.length() > 20) {
            value = value.substr(0, 20);
        }
        return Token(TOKEN_IDENTIFIER, value, startLine);
    }
}

Token Lexer::scanNumber() {
    std::string value;
    int startLine = line;
    
    while (pos < source.length()) {
        char c = currentChar();
        if (isDigit(c)) {
            value += c;
            nextChar();
        } else {
            break;
        }
    }
    
    return Token(TOKEN_CONSTANT, value, startLine);
}

Token Lexer::scanString() {
    std::string value = "\"";
    int startLine = line;
    nextChar(); // 跳过开始的引号
    
    while (pos < source.length()) {
        char c = currentChar();
        if (c == '\0') {
            errorCount++;
            break;
        } else if (c == '"') {
            value += c;
            nextChar();
            break;
        } else if (c == '\\') {
            value += c;
            nextChar();
            if (pos < source.length()) {
                value += currentChar();
                nextChar();
            }
        } else {
            value += c;
            nextChar();
        }
    }
    
    return Token(TOKEN_CONSTANT, value, startLine);
}

Token Lexer::scanOperator() {
    std::string value;
    int startLine = line;
    char c = currentChar();
    
    value += c;
    nextChar();
    
    // 处理双字符运算符
    if (c == '>' || c == '<' || c == '!' || c == '=') {
        char next = currentChar();
        if (next == '=') {
            value += next;
            nextChar();
        } else if (c == '>' && next == '>') {
            value += next;
            nextChar();
        } else if (c == '<' && next == '<') {
            value += next;
            nextChar();
        }
    } else if (c == '+' || c == '-') {
        char next = currentChar();
        if (next == '+' || next == '=') {
            value += next;
            nextChar();
        }
    } else if (c == '*' || c == '/') {
        char next = currentChar();
        if (next == '=') {
            value += next;
            nextChar();
        }
    }
    
    return Token(TOKEN_OPERATOR, value, startLine);
}

Token Lexer::scanDelimiter() {
    std::string value;
    int startLine = line;
    value += currentChar();
    nextChar();
    return Token(TOKEN_DELIMITER, value, startLine);
}

Token Lexer::getNextToken() {
    skipWhitespace();
    
    if (pos >= source.length()) {
        return Token(TOKEN_DELIMITER, "", line);
    }
    
    char c = currentChar();
    
    // 识别标识符或保留字
    if (isLetter(c)) {
        return scanIdentifierOrKeyword();
    }
    
    // 识别数字
    if (isDigit(c)) {
        return scanNumber();
    }
    
    // 识别字符串常量
    if (c == '"') {
        return scanString();
    }
    
    // 识别运算符
    if (c == '+' || c == '-' || c == '*' || c == '/' || 
        c == '=' || c == '>' || c == '<' || c == '!') {
        return scanOperator();
    }
    
    // 识别分隔符
    if (c == ',' || c == ';' || c == '{' || c == '}' || 
        c == '(' || c == ')' || c == '[' || c == ']') {
        return scanDelimiter();
    }
    
    // 未识别的字符，作为错误处理
    errorCount++;
    std::string errorChar;
    errorChar += c;
    nextChar();
    return Token(TOKEN_DELIMITER, errorChar, line);
}

bool Lexer::hasMoreTokens() {
    skipWhitespace();
    return pos < source.length();
}

int Lexer::getErrorCount() const {
    return errorCount;
}

