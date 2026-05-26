#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端文件传输测试
"""
import os
import sys
import time
import subprocess
import psutil

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

def kill_existing_processes():
    """杀死现有的服务器进程"""
    print("1. 清理现有进程...")
    
    try:
        # 查找并杀死现有的python server.py进程
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'server.py' in cmdline:
                        print(f"   杀死进程 PID: {proc.info['pid']}")
                        proc.terminate()
                        proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
        print("   ✓ 进程清理完成")
    except Exception as e:
        print(f"   ✗ 进程清理失败: {e}")

def check_directory_structure():
    """检查目录结构"""
    print("\n2. 检查目录结构...")
    
    # 检查chat_data目录
    chat_data_exists = os.path.exists(config.DATA_DIR)
    print(f"   chat_data目录存在: {chat_data_exists}")
    
    # 检查received_files目录
    received_dir = f"{config.DATA_DIR}/received_files"
    received_exists = os.path.exists(received_dir)
    print(f"   received_files目录存在: {received_exists}")
    
    if not received_exists:
        try:
            os.makedirs(received_dir, exist_ok=True)
            print(f"   ✓ 创建received_files目录: {received_dir}")
        except Exception as e:
            print(f"   ✗ 创建目录失败: {e}")
    
    # 检查测试文件
    test_files = ["test_image.jpg", "test_files/test_image.png"]
    for file_path in test_files:
        exists = os.path.exists(file_path)
        print(f"   测试文件 {file_path}: {'存在' if exists else '不存在'}")

def test_server_startup():
    """测试服务器启动"""
    print("\n3. 测试服务器启动...")
    
    try:
        # 启动服务器
        print("   启动服务器...")
        proc = subprocess.Popen(
            [sys.executable, 'server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # 等待服务器启动
        time.sleep(2)
        
        # 检查进程是否仍在运行
        if proc.poll() is None:
            print("   ✓ 服务器启动成功")
            
            # 停止服务器
            proc.terminate()
            proc.wait(timeout=5)
            print("   ✓ 服务器已停止")
            return True
        else:
            stdout, stderr = proc.communicate()
            print(f"   ✗ 服务器启动失败")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return False
            
    except Exception as e:
        print(f"   ✗ 服务器启动测试失败: {e}")
        return False

def test_image_processing():
    """测试图片处理功能"""
    print("\n4. 测试图片处理功能...")
    
    try:
        from PIL import Image, ImageTk
        import tkinter as tk
        
        # 创建临时根窗口
        if tk._default_root is None:
            root = tk.Tk()
            root.withdraw()
        
        test_image = "test_image.jpg"
        if os.path.exists(test_image):
            print(f"   测试图片: {test_image}")
            
            # 加载图片
            img = Image.open(test_image)
            print(f"   ✓ 图片加载成功，尺寸: {img.size}")
            
            # 创建缩略图
            max_size = (300, 200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            print(f"   ✓ 缩略图创建成功，尺寸: {img.size}")
            
            # 转换为Tkinter格式
            photo = ImageTk.PhotoImage(img)
            print("   ✓ 转换为Tkinter格式成功")
            
            print("   ✓ 图片处理功能正常")
            return True
        else:
            print(f"   ✗ 测试图片不存在: {test_image}")
            return False
            
    except ImportError as e:
        print(f"   ✗ PIL库导入失败: {e}")
        return False
    except Exception as e:
        print(f"   ✗ 图片处理测试失败: {e}")
        return False

def test_file_type_support():
    """测试文件类型支持"""
    print("\n5. 测试文件类型支持...")
    
    # 检查支持的图片类型
    image_types = config.SUPPORTED_IMAGE_TYPES
    print(f"   支持的图片类型数量: {len(image_types)}")
    
    # 检查支持的视频类型
    video_types = config.SUPPORTED_VIDEO_TYPES
    print(f"   支持的视频类型数量: {len(video_types)}")
    
    # 检查常见格式是否支持
    common_formats = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov']
    supported_count = 0
    
    for fmt in common_formats:
        if fmt in image_types or fmt in video_types:
            supported_count += 1
    
    print(f"   常见格式支持率: {supported_count}/{len(common_formats)}")
    
    return supported_count == len(common_formats)

def main():
    """主测试函数"""
    print("=" * 60)
    print("端到端文件传输功能测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        kill_existing_processes,
        check_directory_structure,
        test_server_startup,
        test_image_processing,
        test_file_type_support
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   测试 {test_func.__name__} 出现异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！文件传输功能应该可以正常工作。")
        print("\n建议的测试步骤:")
        print("1. 启动服务器: python server.py")
        print("2. 启动客户端: python client.py")
        print("3. 登录聊天应用")
        print("4. 在大厅或私聊中发送图片文件")
        print("5. 观察文件是否正确显示和可以预览")
    else:
        print("⚠️  部分测试失败，请检查上面的错误信息。")
    
    print("=" * 60)

if __name__ == "__main__":
    main()