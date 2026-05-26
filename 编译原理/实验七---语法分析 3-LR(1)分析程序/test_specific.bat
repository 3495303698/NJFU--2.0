@echo off
chcp 65001 > nul

echo 正在测试表达式: i+i#
echo.

echo 创建测试输入文件...
echo 测试用户> test_input.txt
echo 123456>> test_input.txt
echo 计算机科学与技术>> test_input.txt
echo i+i#>> test_input.txt
echo n>> test_input.txt

echo 运行测试...
echo.\lr1_analyzer.exe < test_input.txt
.\lr1_analyzer.exe < test_input.txt > test_output.txt

echo 测试完成！请查看test_output.txt文件获取测试结果。
echo.
echo 清理临时文件...
del test_input.txt

echo 测试输出预览：
echo ----------------------------------------
type test_output.txt | findstr /C:"分析过程" /C:"合法符号串" /C:"非法符号串" /C:"分析出错"
echo ----------------------------------------
echo.
pause