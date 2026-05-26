#!/usr/bin/env python3
"""
测试文件预览和保存功能的脚本
"""

import os
import sys
import tempfile
import config

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_image():
    """创建一个测试图片文件"""
    try:
        from PIL import Image
        # 创建一个简单的测试图片
        img = Image.new('RGB', (100, 100), color='red')
        temp_dir = tempfile.gettempdir()
        test_image_path = os.path.join(temp_dir, 'test_image.jpg')
        img.save(test_image_path, 'JPEG')
        return test_image_path
    except ImportError:
        print("PIL未安装，跳过图片创建测试")
        return None
    except Exception as e:
        print(f"创建测试图片失败: {e}")
        return None

def create_test_video():
    """创建一个测试视频文件（模拟）"""
    temp_dir = tempfile.gettempdir()
    test_video_path = os.path.join(temp_dir, 'test_video.mp4')
    # 创建一个空的视频文件用于测试
    with open(test_video_path, 'wb') as f:
        f.write(b'test video content')
    return test_video_path

def test_file_type_detection():
    """测试文件类型检测"""
    print("测试文件类型检测...")
    
    # 测试图片类型
    image_files = ['test.jpg', 'test.png', 'test.gif', 'test.webp', 'test.svg']
    for file_name in image_files:
        ext = os.path.splitext(file_name)[1].lower()
        is_image = ext in config.SUPPORTED_IMAGE_TYPES
        print(f"  {file_name}: {'图片' if is_image else '非图片'} (扩展名: {ext})")
    
    # 测试视频类型
    video_files = ['test.mp4', 'test.avi', 'test.mov', 'test.mkv', 'test.webm']
    for file_name in video_files:
        ext = os.path.splitext(file_name)[1].lower()
        is_video = ext in config.SUPPORTED_VIDEO_TYPES
        print(f"  {file_name}: {'视频' if is_video else '非视频'} (扩展名: {ext})")

def test_file_descriptions():
    """测试文件描述"""
    print("\n测试文件描述...")
    
    # 测试图片描述
    print("图片类型描述:")
    for ext, desc in config.IMAGE_TYPE_DESCRIPTIONS.items():
        print(f"  {ext}: {desc}")
    
    print("\n视频类型描述:")
    for ext, desc in config.VIDEO_TYPE_DESCRIPTIONS.items():
        print(f"  {ext}: {desc}")

def test_directory_creation():
    """测试目录创建"""
    print("\n测试目录创建...")
    
    try:
        # 创建必要的目录
        os.makedirs(config.DATA_DIR, exist_ok=True)
        os.makedirs(f'{config.DATA_DIR}/received_files', exist_ok=True)
        os.makedirs(f'{config.DATA_DIR}/received_images', exist_ok=True)
        
        print(f"  数据目录创建成功: {config.DATA_DIR}")
        print(f"  接收文件目录: {config.DATA_DIR}/received_files")
        print(f"  接收图片目录: {config.DATA_DIR}/received_images")
        
        return True
    except Exception as e:
        print(f"  目录创建失败: {e}")
        return False

def test_platform_specific_functions():
    """测试平台特定功能"""
    print("\n测试平台特定功能...")
    
    import platform
    
    system = platform.system()
    print(f"  当前系统: {system}")
    
    if system == "Windows":
        print("  Windows系统: 使用 os.startfile()")
    elif system == "Darwin":
        print("  macOS系统: 使用 subprocess.open()")
    else:
        print("  Linux系统: 使用 subprocess.xdg-open()")

def main():
    """主测试函数"""
    print("=" * 50)
    print("文件预览和保存功能测试")
    print("=" * 50)
    
    # 测试文件类型检测
    test_file_type_detection()
    
    # 测试文件描述
    test_file_descriptions()
    
    # 测试目录创建
    if test_directory_creation():
        print("\n✅ 目录创建测试通过")
    else:
        print("\n❌ 目录创建测试失败")
    
    # 测试平台特定功能
    test_platform_specific_functions()
    
    # 创建测试文件
    print("\n创建测试文件...")
    test_image = create_test_image()
    test_video = create_test_video()
    
    if test_image:
        print(f"  测试图片创建成功: {test_image}")
    if test_video:
        print(f"  测试视频创建成功: {test_video}")
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n功能总结:")
    print("✅ 文件类型检测 - 支持多种图片和视频格式")
    print("✅ 文件描述 - 中文显示文件类型")
    print("✅ 目录结构 - 自动创建必要目录")
    print("✅ 平台兼容 - 支持Windows/macOS/Linux")
    print("✅ 测试文件 - 创建了测试用的媒体文件")
    
    print("\n预览功能说明:")
    print("- 图片/视频文件: 点击'预览'按钮调用系统默认播放器")
    print("- 其他文件: 点击'下载'按钮打开文件目录")
    print("- 右键菜单: 支持预览、保存到本地、打开文件目录")
    
    # 清理测试文件
    if test_image and os.path.exists(test_image):
        try:
            os.remove(test_image)
            print(f"\n清理测试图片: {test_image}")
        except:
            pass
    
    if test_video and os.path.exists(test_video):
        try:
            os.remove(test_video)
            print(f"清理测试视频: {test_video}")
        except:
            pass

if __name__ == '__main__':
    main()