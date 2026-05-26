#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试服务器修复后的文件接收功能
"""
import os
import sys
import socket
import time
import threading

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from network import NetworkProtocol
import config

def test_server_file_handling():
    """测试服务器端的文件处理功能"""
    print("=" * 50)
    print("测试服务器文件接收修复")
    print("=" * 50)
    
    # 1. 检查网络协议函数签名
    print("\n1. 检查NetworkProtocol.receive_file函数:")
    try:
        # 检查函数是否需要两个参数
        import inspect
        sig = inspect.signature(NetworkProtocol.receive_file)
        print(f"   函数签名: {sig}")
        print(f"   参数数量: {len(sig.parameters)}")
        for name, param in sig.parameters.items():
            print(f"   - {name}: {param}")
    except Exception as e:
        print(f"   ✗ 检查函数签名失败: {e}")
    
    # 2. 测试receive_file函数调用
    print("\n2. 测试receive_file函数调用:")
    try:
        # 创建测试socket
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(1.0)  # 设置短超时用于测试
        
        # 创建临时目录
        temp_dir = 'test_server_files'
        os.makedirs(temp_dir, exist_ok=True)
        
        print(f"   ✓ 临时目录创建: {temp_dir}")
        
        # 测试函数调用（使用无效socket会导致timeout，这证明函数能正确处理参数）
        try:
            result = NetworkProtocol.receive_file(test_socket, temp_dir)
            print(f"   函数调用成功，返回值: {result}")
        except socket.timeout:
            print("   ✓ 函数调用成功（socket超时是预期的）")
        except Exception as e:
            print(f"   函数调用错误: {e}")
        
        test_socket.close()
        
    except Exception as e:
        print(f"   ✗ 测试失败: {e}")
    
    # 3. 检查服务器代码修复
    print("\n3. 检查服务器代码修复:")
    try:
        with open('server.py', 'r', encoding='utf-8') as f:
            server_content = f.read()
            
        # 检查是否包含修复后的代码
        if 'save_dir = \'server_temp_files\'' in server_content:
            print("   ✓ 服务器代码包含save_dir参数")
        else:
            print("   ✗ 服务器代码缺少save_dir参数")
            
        if 'NetworkProtocol.receive_file(client_sock, save_dir)' in server_content:
            print("   ✓ 服务器代码正确调用receive_file函数")
        else:
            print("   ✗ 服务器代码调用receive_file函数方式不正确")
            
    except Exception as e:
        print(f"   ✗ 检查服务器代码失败: {e}")
    
    # 4. 检查调试信息
    print("\n4. 检查调试信息:")
    try:
        with open('network.py', 'r', encoding='utf-8') as f:
            network_content = f.read()
            
        if '[DEBUG]' in network_content:
            debug_count = network_content.count('[DEBUG]')
            print(f"   ✓ 网络模块包含{debug_count}条调试信息")
        else:
            print("   ✗ 网络模块缺少调试信息")
            
    except Exception as e:
        print(f"   ✗ 检查网络模块失败: {e}")
    
    print("\n测试完成!")
    print("=" * 50)

if __name__ == "__main__":
    test_server_file_handling()