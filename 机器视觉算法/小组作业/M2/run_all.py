#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
立体匹配蒸馏框架 - 完整功能启动脚本（修复编码问题）
"""

import os
import sys
import subprocess
import time
import argparse

def run_command(command, description):
    """运行命令并显示状态（修复编码问题）"""
    print(f"\n{'='*60}")
    print(f"步骤: {description}")
    print(f"命令: {command}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        # 修复编码问题：使用UTF-8编码
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8',  # 明确指定UTF-8编码
            errors='ignore'    # 忽略无法解码的字符
        )

        # 实时输出
        for line in process.stdout:
            print(line, end='', flush=True)

        # 等待完成
        return_code = process.wait()

        elapsed_time = time.time() - start_time

        if return_code == 0:
            print(f"✓ {description} 完成 (耗时: {elapsed_time:.2f}秒)")
            return True
        else:
            print(f"✗ {description} 失败 (返回码: {return_code})")
            return False

    except Exception as e:
        print(f"✗ {description} 异常: {str(e)}")
        return False

def run_python_script(script_name, description, args=""):
    """直接运行Python脚本（避免编码问题）"""
    print(f"\n{'='*60}")
    print(f"步骤: {description}")
    print(f"脚本: {script_name}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        # 直接导入并运行脚本
        if script_name == "test_models.py":
            from test_models import main as test_main
            test_main()
        elif script_name == "demo.py":
            from demo import main as demo_main
            demo_main()
        elif script_name == "run_train.py":
            from run_train import main as train_main
            # 解析参数
            import shlex
            train_args = shlex.split(args)
            sys.argv = ['run_train.py'] + train_args
            train_main()
        elif script_name == "run_eval.py":
            from run_eval import main as eval_main
            # 解析参数
            import shlex
            eval_args = shlex.split(args)
            sys.argv = ['run_eval.py'] + eval_args
            eval_main()

        elapsed_time = time.time() - start_time
        print(f"✓ {description} 完成 (耗时: {elapsed_time:.2f}秒)")
        return True

    except Exception as e:
        print(f"✗ {description} 异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description="立体匹配蒸馏框架完整启动脚本")
    parser.add_argument("--epochs", type=int, default=3, help="训练轮数")
    parser.add_argument("--batch-size", type=int, default=2, help="批次大小")
    parser.add_argument("--skip-train", action="store_true", help="跳过训练步骤")

    args = parser.parse_args()

    print("\n" + "="*70)
    print("立体匹配蒸馏框架 - 完整功能启动（修复编码版）")
    print("="*70)
    print(f"参数: epochs={args.epochs}, batch_size={args.batch_size}")
    print("="*70)

    # 检查必要的脚本文件
    required_scripts = ['test_models.py', 'demo.py', 'run_train.py', 'run_eval.py']
    missing_scripts = []

    for script in required_scripts:
        if not os.path.exists(script):
            missing_scripts.append(script)

    if missing_scripts:
        print(f"错误: 缺少必要的脚本文件: {missing_scripts}")
        print("请确保以下文件存在于当前目录:")
        for script in missing_scripts:
            print(f"  - {script}")
        return

    # 步骤1: 测试模型和数据加载器
    if not run_python_script("test_models.py", "测试模型和数据加载器"):
        print("警告: 模型测试失败，但继续执行...")

    # 步骤2: 运行演示（在训练前查看初始效果）
    if not run_python_script("demo.py", "运行初始演示"):
        print("警告: 初始演示失败，但继续执行...")

    # 步骤3: 训练模型（可选跳过）
    if not args.skip_train:
        train_args = f"--epochs {args.epochs} --batch-size {args.batch_size} --lr 0.001"
        if not run_python_script("run_train.py", f"训练模型 ({args.epochs}个epoch)", train_args):
            print("错误: 训练失败!")
            return
    else:
        print("\n跳过训练步骤...")

    # 步骤4: 查找最新的模型文件
    print("\n查找训练好的模型...")
    checkpoint_dir = "checkpoints"
    model_files = []

    if os.path.exists(checkpoint_dir):
        for file in os.listdir(checkpoint_dir):
            if file.endswith('.pth') and 'student' in file:
                model_files.append(os.path.join(checkpoint_dir, file))

    if model_files:
        # 按修改时间排序，获取最新的模型
        model_files.sort(key=os.path.getmtime, reverse=True)
        latest_model = model_files[0]
        print(f"找到模型: {latest_model}")

        # 步骤5: 评估模型
        eval_args = f'--model-path "{latest_model}" --batch-size {args.batch_size}'
        if not run_python_script("run_eval.py", "评估训练好的模型", eval_args):
            print("警告: 模型评估失败!")

        # 步骤6: 最终演示（使用训练好的模型）
        print("\n准备最终演示...")

        # 直接运行最终演示代码
        try:
            import torch
            import matplotlib.pyplot as plt
            from stereo_distillation.models.student import StudentModel
            from stereo_distillation.data.dataloader import get_dataloader

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"使用设备: {device}")

            # 加载训练好的模型
            model = StudentModel().to(device)
            checkpoint = torch.load(latest_model, map_location=device)
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            else:
                model.load_state_dict(checkpoint)
            model.eval()
            print("训练好的模型加载成功!")

            # 获取测试数据
            dataloader = get_dataloader(batch_size=1, train=False)
            left_img, right_img, disparity = next(iter(dataloader))

            left_img = left_img.to(device)
            right_img = right_img.to(device)
            disparity = disparity.to(device)

            # 推理
            with torch.no_grad():
                student_output = model(left_img, right_img)

            # 可视化
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))

            left_np = left_img[0].permute(1, 2, 0).cpu().numpy()
            right_np = right_img[0].permute(1, 2, 0).cpu().numpy()
            pred_np = student_output[0, 0].cpu().numpy()
            gt_np = disparity[0, 0].cpu().numpy()

            axes[0, 0].imshow(left_np)
            axes[0, 0].set_title("左图像")
            axes[0, 0].axis('off')

            axes[0, 1].imshow(right_np)
            axes[0, 1].set_title("右图像")
            axes[0, 1].axis('off')

            im1 = axes[1, 0].imshow(pred_np, cmap='viridis')
            axes[1, 0].set_title("训练后预测视差")
            axes[1, 0].axis('off')
            plt.colorbar(im1, ax=axes[1, 0])

            im2 = axes[1, 1].imshow(gt_np, cmap='viridis')
            axes[1, 1].set_title("真实视差")
            axes[1, 1].axis('off')
            plt.colorbar(im2, ax=axes[1, 1])

            plt.tight_layout()
            plt.savefig('final_demo_result.png', dpi=150, bbox_inches='tight')
            print("最终演示结果已保存: final_demo_result.png")
            plt.show()

            print("✓ 最终演示完成")

        except Exception as e:
            print(f"✗ 最终演示失败: {str(e)}")
            import traceback
            traceback.print_exc()

    else:
        print("未找到训练好的模型，跳过评估和最终演示")

    # 步骤7: 生成总结报告
    print("\n" + "="*70)
    print("立体匹配蒸馏框架 - 完整流程执行完成!")
    print("="*70)
    print("\n生成的文件:")
    print("  - checkpoints/          : 训练好的模型")
    if os.path.exists('final_demo_result.png'):
        print("  - final_demo_result.png : 最终演示结果（使用训练好的模型）")
    print("\n下一步建议:")
    print("  1. 查看生成的图像结果")
    print("  2. 调整参数重新训练: python run_all_fixed.py --epochs 10 --batch-size 4")
    print("  3. 添加真实数据集支持")
    print("  4. 改进模型架构")
    print("="*70)

if __name__ == "__main__":
    main()