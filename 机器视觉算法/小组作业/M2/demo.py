#!/usr/bin/env python
"""
立体匹配演示脚本
"""

import torch
import matplotlib.pyplot as plt
import numpy as np
from stereo_distillation.models.teacher import TeacherModel
from stereo_distillation.models.student import StudentModel
from stereo_distillation.data.dataloader import get_dataloader

def visualize_results(left_img, right_img, pred_disp, gt_disp, save_path=None):
    """可视化结果"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # 转换为numpy并调整维度
    left_np = left_img[0].permute(1, 2, 0).cpu().numpy()
    right_np = right_img[0].permute(1, 2, 0).cpu().numpy()
    pred_np = pred_disp[0, 0].cpu().numpy()
    gt_np = gt_disp[0, 0].cpu().numpy()

    # 显示图像
    axes[0, 0].imshow(left_np)
    axes[0, 0].set_title("左图像")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(right_np)
    axes[0, 1].set_title("右图像")
    axes[0, 1].axis('off')

    # 显示视差图
    im1 = axes[1, 0].imshow(pred_np, cmap='viridis')
    axes[1, 0].set_title("预测视差")
    axes[1, 0].axis('off')
    plt.colorbar(im1, ax=axes[1, 0])

    im2 = axes[1, 1].imshow(gt_np, cmap='viridis')
    axes[1, 1].set_title("真实视差")
    axes[1, 1].axis('off')
    plt.colorbar(im2, ax=axes[1, 1])

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"结果已保存: {save_path}")

    plt.show()

def main():
    print("=" * 50)
    print("立体匹配演示")
    print("=" * 50)

    # 检查GPU可用性
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    # 初始化模型
    teacher = TeacherModel().to(device)
    student = StudentModel().to(device)

    # 加载一个批次的数据
    dataloader = get_dataloader(batch_size=1, train=False)
    left_img, right_img, disparity = next(iter(dataloader))

    left_img = left_img.to(device)
    right_img = right_img.to(device)
    disparity = disparity.to(device)

    print(f"输入形状: 左图 {left_img.shape}, 右图 {right_img.shape}, 视差 {disparity.shape}")

    # 推理
    with torch.no_grad():
        print("\n教师模型推理...")
        teacher_output = teacher(left_img, right_img)
        print(f"教师输出形状: {teacher_output.shape}")

        print("学生模型推理...")
        student_output = student(left_img, right_img)
        print(f"学生输出形状: {student_output.shape}")

    # 可视化结果
    print("\n可视化结果...")
    visualize_results(
        left_img.cpu(),
        right_img.cpu(),
        student_output.cpu(),
        disparity.cpu(),
        save_path="demo_result.png"
    )

    # 计算基本指标
    from stereo_distillation.utils.metrics import compute_metrics
    metrics = compute_metrics(student_output, disparity)

    print("\n单样本评估指标:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    print("=" * 50)
    print("演示完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()