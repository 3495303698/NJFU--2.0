#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的文件传输修复验证测试
"""
import os
import sys
import time
import subprocess

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

def check_fixes():
    """检查所有修复是否生效"""
    print("=" * 50)
    print("文件传输修复验证")
    print("=" * 50)
    
    fixes_verified = 0
    total_fixes = 4
    
    # 1. 检查服务器文件接收修复
    print("\n1. 检查服务器文件接收修复:")
    try:
        with open('server.py', 'r', encoding='utf-8') as f:
            server_content = f.read()
        
        if 'save_dir = \'server_temp_files\'' in server_content:
            print("   ✅ 服务器save_dir参数已修复")
            fixes_verified += 1
        else:
            print("   ❌ 服务器save_dir参数未修复")
        
        if 'NetworkProtocol.receive_file(client_sock, save_dir)' in server_content:
            print("   ✅ 服务器receive_file调用已修复")
            fixes_verified += 1
        else:
            print("   ❌ 服务器receive_file调用未修复")
    except Exception as e:
        print(f"   ❌ 检查服务器代码失败: {e}")
    
    # 2. 检查网络模块调试信息
    print("\n2. 检查网络模块调试信息:")
    try:
        with open('network.py', 'r', encoding='utf-8') as f:
            network_content = f.read()
        
        debug_count = network_content.count('[DEBUG]')
        if debug_count > 10:
            print(f"   ✅ 网络模块包含{debug_count}条调试信息")
            fixes_verified += 1
        else:
            print("   ❌ 网络模块调试信息不足")
    except Exception as e:
        print(f"   ❌ 检查网络模块失败: {e}")
    
    # 3. 检查客户端文件显示修复
    print("\n3. 检查客户端文件显示修复:")
    try:
        with open('client.py', 'r', encoding='utf-8') as f:
            client_content = f.read()
        
        if '_show_file被调用' in client_content:
            print("   ✅ 客户端文件显示调试信息已添加")
            fixes_verified += 1
        else:
            print("   ❌ 客户端文件显示调试信息未添加")
    except Exception as e:
        print(f"   ❌ 检查客户端代码失败: {e}")
    
    # 4. 检查目录结构
    print("\n4. 检查目录结构:")
    try:
        received_dir = f"{config.DATA_DIR}/received_files"
        if not os.path.exists(received_dir):
            os.makedirs(received_dir, exist_ok=True)
            print(f"   ✅ 创建received_files目录: {received_dir}")
        else:
            print(f"   ✅ received_files目录已存在: {received_dir}")
        
        files = os.listdir(received_dir)
        print(f"   ℹ️  接收目录内容: {files}")
        
    except Exception as e:
        print(f"   ❌ 检查目录结构失败: {e}")
    
    print(f"\n修复验证结果: {fixes_verified}/{total_fixes}")
    
    if fixes_verified == total_fixes:
        print("\n🎉 所有修复已完成！")
        print("\n建议的测试步骤:")
        print("1. 确保服务器正在运行")
        print("2. 启动客户端: python client.py")
        print("3. 登录并发送文件")
        print("4. 观察控制台调试信息")
        print("5. 检查文件是否正确保存和显示")
    else:
        print("\n⚠️  部分修复未完成，请检查上面的问题")
    
    print("=" * 50)

if __name__ == "__main__":
    check_fixes()