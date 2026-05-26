# Makefile for 递归下降分析程序

CXX = g++
CXXFLAGS = -Wall -std=c++11
INCLUDES = -I include
SOURCES = src/main.cpp src/parser.cpp
TARGET = parser.exe

# Windows 默认目标
all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(TARGET)

# 清理编译产物
clean:
	rm -f $(TARGET) *.o

# 运行程序
run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
