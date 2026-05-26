cmake_minimum_required(VERSION 3.10)
project(LexicalAnalyzer)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 添加可执行文件
add_executable(词法分析器 main.cpp lexer.cpp lexer.h)

# Windows下使用中文输出
if(WIN32)
    set_target_properties(词法分析器 PROPERTIES
        LINK_FLAGS "/SUBSYSTEM:CONSOLE"
    )
endif()

