@echo off
chcp 65001 > nul

echo 生成测试输入文件...
echo 测试用户 > test_run_input.txt
echo 2024001 > test_run_input.txt
echo 计算机科学1班 >> test_run_input.txt
echo i+i# >> test_run_input.txt
echo n >> test_run_input.txt

echo 正在运行LR(1)语法分析器测试...
echo 测试结果将保存到test_results.txt

type test_run_input.txt | lr1_analyzer.exe > test_results.txt

echo 测试完成！请查看test_results.txt获取详细输出。