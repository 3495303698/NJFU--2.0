@echo off

rem LR(1)语法分析器测试脚本

echo =======================================================
echo LR(1)语法分析器测试脚本
echo =======================================================
echo

echo 测试用例1: 简单表达式 i+i#
echo ----------------------------------------
echo 张政笑> input.txt
echo 20230001>> input.txt
echo 计算机科学与技术1班>> input.txt
echo i+i#>> input.txt
echo n>> input.txt
lr1_analyzer < input.txt

rem 等待用户按键继续
echo.
echo 按任意键继续下一个测试...
pause > nul

echo

echo 测试用例2: 带括号的表达式 i*(i+i)#
echo ----------------------------------------
echo 张政笑> input.txt
echo 20230001>> input.txt
echo 计算机科学与技术1班>> input.txt
echo i*(i+i)#>> input.txt
echo n>> input.txt
lr1_analyzer < input.txt

rem 等待用户按键继续
echo.
echo 按任意键继续下一个测试...
pause > nul

echo

echo 测试用例3: 复杂表达式 i+i*i-i/i#
echo ----------------------------------------
echo 张政笑> input.txt
echo 20230001>> input.txt
echo 计算机科学与技术1班>> input.txt
echo i+i*i-i/i#>> input.txt
echo n>> input.txt
lr1_analyzer < input.txt

rem 等待用户按键继续
echo.
echo 按任意键继续下一个测试...
pause > nul

echo

echo 测试用例4: 错误表达式 i+#（缺少操作数）
echo ----------------------------------------
echo 张政笑> input.txt
echo 20230001>> input.txt
echo 计算机科学与技术1班>> input.txt
echo i+#>> input.txt
echo n>> input.txt
lr1_analyzer < input.txt

rem 等待用户按键继续
echo.
echo 按任意键继续下一个测试...
pause > nul

echo

echo 测试用例5: 错误表达式 i+(i#（括号不匹配）
echo ----------------------------------------
echo 张政笑> input.txt
echo 20230001>> input.txt
echo 计算机科学与技术1班>> input.txt
echo i+(i#>> input.txt
echo n>> input.txt
lr1_analyzer < input.txt

echo.
echo 所有测试用例执行完毕！
pause