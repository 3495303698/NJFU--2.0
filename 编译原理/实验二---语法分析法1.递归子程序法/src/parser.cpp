#include "../include/parser.h"
#include <cctype>

Parser::Parser(const std::string& inputStr) 
    : input(inputStr), pos(0), currentToken(TOKEN_ERROR), hasError(false) {
    nextToken();
}

void Parser::nextToken() {
    // 跳过空白字符
    while (pos < input.length() && (input[pos] == ' ' || input[pos] == '\t' || input[pos] == '\n')) {
        pos++;
    }
    
    // 检查是否到达字符串末尾
    if (pos >= input.length()) {
        currentToken = TOKEN_ERROR;
        if (!hasError) {
            error("输入字符串未以 # 结束");
        }
        return;
    }
    
    char ch = input[pos];
    
    switch (ch) {
        case '+':
            currentToken = TOKEN_PLUS;
            pos++;
            break;
        case '-':
            currentToken = TOKEN_MINUS;
            pos++;
            break;
        case '*':
            currentToken = TOKEN_MULTIPLY;
            pos++;
            break;
        case '/':
            currentToken = TOKEN_DIVIDE;
            pos++;
            break;
        case '(':
            currentToken = TOKEN_LPAREN;
            pos++;
            break;
        case ')':
            currentToken = TOKEN_RPAREN;
            pos++;
            break;
        case 'i':
            currentToken = TOKEN_IDENTIFIER;
            pos++;
            break;
        case '#':
            currentToken = TOKEN_END;
            pos++;
            break;
        default:
            currentToken = TOKEN_ERROR;
            error("遇到非法字符: '" + std::string(1, ch) + "' (位置: " + std::to_string(pos + 1) + ")");
            break;
    }
}

void Parser::error(const std::string& msg) {
    hasError = true;
    if (errorMsg.empty()) {
        errorMsg = msg;
    } else {
        errorMsg += "; " + msg;
    }
}

// E -> TG
void Parser::E() {
    if (hasError) return;
    T();
    if (hasError) return;
    G();
}

// G -> +TG | -TG | ε
void Parser::G() {
    if (hasError) return;
    
    if (currentToken == TOKEN_PLUS) {
        nextToken();
        T();
        if (hasError) return;
        G();
    } else if (currentToken == TOKEN_MINUS) {
        nextToken();
        T();
        if (hasError) return;
        G();
    }
    // else: ε (空产生式，直接返回)
}

// T -> FS
void Parser::T() {
    if (hasError) return;
    F();
    if (hasError) return;
    S();
}

// S -> *FS | /FS | ε
void Parser::S() {
    if (hasError) return;
    
    if (currentToken == TOKEN_MULTIPLY) {
        nextToken();
        F();
        if (hasError) return;
        S();
    } else if (currentToken == TOKEN_DIVIDE) {
        nextToken();
        F();
        if (hasError) return;
        S();
    }
    // else: ε (空产生式，直接返回)
}

// F -> (E) | i
void Parser::F() {
    if (hasError) return;
    
    if (currentToken == TOKEN_LPAREN) {
        nextToken();
        E();
        if (hasError) return;
        
        if (currentToken == TOKEN_RPAREN) {
            nextToken();
        } else {
            std::string msg = "期望 ')' 但遇到: ";
            if (currentToken == TOKEN_END) {
                msg += "结束符 #";
            } else if (currentToken == TOKEN_ERROR) {
                msg += "非法字符或字符串结束";
            } else {
                msg += "其他字符 (位置: " + std::to_string(pos + 1) + ")";
            }
            error(msg);
        }
    } else if (currentToken == TOKEN_IDENTIFIER) {
        nextToken();
    } else {
        std::string msg = "期望标识符 'i' 或 '(' 但遇到: ";
        if (currentToken == TOKEN_END) {
            msg += "结束符 #";
        } else if (currentToken == TOKEN_ERROR) {
            msg += "非法字符或字符串结束";
        } else {
            msg += "其他字符 (位置: " + std::to_string(pos + 1) + ")";
        }
        error(msg);
    }
}

bool Parser::parse() {
    hasError = false;
    errorMsg.clear();
    pos = 0;
    nextToken();
    
    E();
    
    if (!hasError && currentToken != TOKEN_END) {
        if (pos < input.length()) {
            error("分析完成但未到达结束符 #，仍有未处理的字符 (位置: " + std::to_string(pos + 1) + ")");
        } else {
            error("分析完成但输入字符串未以 # 结束");
        }
    }
    
    return !hasError;
}
