#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试LL(1)分析器的功能
"""

from ll1_parser import LL1Parser

def test_parser():
    """
    测试LL(1)分析器的各种情况
    """
    parser = LL1Parser()
    
    # 测试用例列表
    test_cases = [
        # 合法表达式
        ("i#", True, "简单标识符"),
        ("i+i#", True, "加法表达式"),
        ("i-i#", True, "减法表达式"),
        ("i*i#", True, "乘法表达式"),
        ("i/i#", True, "除法表达式"),
        ("i+i+i#", True, "连续加法"),
        ("i*i+i#", True, "乘加混合"),
        ("(i)#", True, "括号表达式"),
        ("(i+i)#", True, "括号内加法"),
        ("i+(i*i)#", True, "复杂表达式1"),
        ("(i+i)*(i-i)#", True, "复杂表达式2"),
        
        # 非法表达式
        ("", False, "空输入"),
        ("i", False, "缺少结束符"),
        ("i++i#", False, "连续加号"),
        ("i+#", False, "不完整表达式1"),
        ("i(i)#", False, "缺少运算符"),
        ("(i#", False, "括号不匹配1"),
        ("i)#", False, "括号不匹配2"),
        ("i@i#", False, "非法字符"),
        ("i++i#", False, "连续运算符"),
    ]
    
    print("开始测试LL(1)分析器...\n")
    success_count = 0
    failure_count = 0
    
    for i, (input_str, expected, description) in enumerate(test_cases, 1):
        print(f"测试 {i}: {description}")
        print(f"  输入: '{input_str}'")
        print(f"  期望结果: {'合法' if expected else '非法'}")
        
        try:
            steps, actual, error_msg = parser.parse(input_str)
            
            # 验证结果是否符合预期
            if actual == expected:
                print(f"  ✓ 测试通过")
                success_count += 1
            else:
                print(f"  ✗ 测试失败: 期望{'合法' if expected else '非法'}，实际{'合法' if actual else '非法'}")
                failure_count += 1
                
                # 打印错误信息（如果有）
                if not actual:
                    print(f"  错误信息: {error_msg}")
                    
                # 打印最后几步分析过程
                print("  分析过程（最后5步）:")
                for step in steps[-5:]:
                    print(f"    步骤 {step['step']}: 栈={step['stack']}, 输入={step['input']}, 动作={step['production']}")
            
        except Exception as e:
            print(f"  ✗ 测试异常: {str(e)}")
            failure_count += 1
        
        print()
    
    # 打印测试结果摘要
    print("测试结果摘要:")
    print(f"  总测试用例数: {len(test_cases)}")
    print(f"  通过: {success_count}")
    print(f"  失败: {failure_count}")
    
    if failure_count == 0:
        print("🎉 所有测试用例通过！")
    else:
        print("❌ 存在测试失败，请检查代码。")
    
    return failure_count == 0

if __name__ == "__main__":
    # 执行测试
    all_passed = test_parser()
    
    # 根据测试结果设置退出码
    import sys
    sys.exit(0 if all_passed else 1)