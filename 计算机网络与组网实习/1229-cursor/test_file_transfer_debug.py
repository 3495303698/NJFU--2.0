#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件传输调试测试脚本
"""
import os
import sys
import time
import socket
import threading
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from network import NetworkProtocol

def test_file_transfer():
    """测试文件传输功能"""
    print("=" * 50)
    print("开始文件传输测试")
    print("=" * 50)
    
    # 1. 检查测试文件
    test_files = [
        "test_image.jpg",
        "test_files/test_image.png", 
        "test_files/test_video.mp4"
    ]
    
    print("\n1. 检查测试文件:")
    for file_path in test_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"  ✓ {file_path} - {file_size} bytes")
        else:
            print(f"  ✗ {file_path} - 文件不存在")
    
    # 2. 检查目录结构
    print("\n2. 检查目录结构:")
    print(f"  DATA_DIR: {config.DATA_DIR}")
    print(f"  目录存在: {os.path.exists(config.DATA_DIR)}")
    
    received_dir = f"{config.DATA_DIR}/received_files"
    print(f"  接收目录: {received_dir}")
    print(f"  接收目录存在: {os.path.exists(received_dir)}")
    
    if os.path.exists(received_dir):
        files = os.listdir(received_dir)
        print(f"  接收目录内容: {files}")
    
    # 3. 测试文件信息解析
    print("\n3. 测试文件信息解析:")
    for file_path in test_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # 确定文件类型
            file_type = 'unknown'
            if file_ext in config.SUPPORTED_IMAGE_TYPES:
                file_type = 'image'
            elif file_ext in config.SUPPORTED_VIDEO_TYPES:
                file_type = 'video'
            elif file_ext in config.SUPPORTED_AUDIO_TYPES:
                file_type = 'audio'
            elif file_ext in config.SUPPORTED_DOCUMENT_TYPES:
                file_type = 'document'
            elif file_ext in config.SUPPORTED_ARCHIVE_TYPES:
                file_type = 'archive'
            
            print(f"  文件: {file_name}")
            print(f"    大小: {file_size} bytes")
            print(f"    扩展名: {file_ext}")
            print(f"    类型: {file_type}")
            print(f"    是否支持: {file_ext in config.SUPPORTED_IMAGE_TYPES or file_ext in config.SUPPORTED_VIDEO_TYPES}")
    
    # 4. 测试文件接收函数
    print("\n4. 测试文件接收函数:")
    test_image = "test_image.jpg"
    if os.path.exists(test_image):
        print(f"  测试图片存在: {test_image}")
        
        # 模拟文件接收过程
        save_dir = f"{config.DATA_DIR}/received_files"
        print(f"  模拟保存目录: {save_dir}")
        print(f"  目录创建成功: {os.makedirs(save_dir, exist_ok=True) is None}")
        
        # 测试文件名冲突处理
        base_name = os.path.splitext(test_image)[0]
        ext = os.path.splitext(test_image)[1]
        counter = 1
        save_path = os.path.join(save_dir, test_image)
        
        while os.path.exists(save_path):
            new_name = f"{base_name}_{counter}{ext}"
            save_path = os.path.join(save_dir, new_name)
            counter += 1
        
        print(f"  模拟保存路径: {save_path}")
    else:
        print(f"  测试图片不存在: {test_image}")
    
    # 5. 测试网络协议
    print("\n5. 测试网络协议:")
    try:
        # 创建一个测试socket
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("  ✓ Socket创建成功")
        test_socket.close()
    except Exception as e:
        print(f"  ✗ Socket创建失败: {e}")
    
    print("\n测试完成!")
    print("=" * 50)

def test_image_display():
    """测试图片显示功能"""
    print("\n" + "=" * 50)
    print("测试图片显示功能")
    print("=" * 50)
    
    try:
        from PIL import Image, ImageTk
        import tkinter as tk
        print("✓ PIL库导入成功")
        
        # 测试图片加载
        test_image = "test_image.jpg"
        if os.path.exists(test_image):
            print(f"✓ 测试图片存在: {test_image}")
            
            img = Image.open(test_image)
            print(f"✓ 图片加载成功，尺寸: {img.size}")
            
            # 创建缩略图
            max_size = (300, 200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            print(f"✓ 缩略图创建成功，尺寸: {img.size}")
            
            # 转换为Tkinter格式
            if tk._default_root is None:
                root = tk.Tk()
                root.withdraw()  # 隐藏窗口
                print("✓ Tkinter根窗口创建成功")
            
            photo = ImageTk.PhotoImage(img)
            print("✓ 转换为Tkinter格式成功")
            
            # 测试事件绑定
            print("✓ 图片处理流程正常")
            
        else:
            print(f"✗ 测试图片不存在: {test_image}")
            
    except ImportError as e:
        print(f"✗ PIL库导入失败: {e}")
    except Exception as e:
        print(f"✗ 图片显示测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("开始文件传输调试测试")
    print(f"当前时间: {datetime.now()}")
    print(f"当前目录: {os.getcwd()}")
    print(f"Python版本: {sys.version}")
    
    test_file_transfer()
    test_image_display()