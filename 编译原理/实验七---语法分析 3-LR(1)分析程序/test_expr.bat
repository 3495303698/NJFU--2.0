@echo off
chcp 65001 > nul

echo 测试用户 > input.txt
echo 123456 >> input.txt
echo 计算机科学与技术 >> input.txt
echo i+i# >> input.txt

REM 运行分析器并将输入重定向
type input.txt | lr1_analyzer.exe > test_output.txt

echo 测试完成，请查看test_output.txt文件获取结果。