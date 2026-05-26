#!/usr/bin/env python
"""
模型功能测试脚本
"""

import torch
from stereo_distillation.models.teacher import TeacherModel
from stereo_distillation.models.student import StudentModel
from stereo_distillation.data.dataloader import get_dataloader

def main():
    print("=" * 50)
    print("模型功能测试")
    print("=" * 50)

    # 检查GPU可用性
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    # 测试模型初始化
    print("\n1. 测试模型初始化...")
    teacher = TeacherModel().to(device)
    student = StudentModel().to(device)
    print("✓ 模型初始化成功")

    # 测试模型参数
    teacher_params = sum(p.numel() for p in teacher.parameters())
    student_params = sum(p.numel() for p in student.parameters())
    print(f"✓ 教师模型参数: {teacher_params}")
    print(f"✓ 学生模型参数: {student_params}")

    # 测试数据加载
    print("\n2. 测试数据加载...")
    dataloader = get_dataloader(batch_size=2, train=True)
    left_img, right_img, disparity = next(iter(dataloader))

    left_img = left_img.to(device)
    right_img = right_img.to(device)
    disparity = disparity.to(device)

    print(f"✓ 数据加载成功")
    print(f"  左图形状: {left_img.shape}")
    print(f"  右图形状: {right_img.shape}")
    print(f"  视差形状: {disparity.shape}")

    # 测试前向传播
    print("\n3. 测试前向传播...")
    with torch.no_grad():
        teacher_output = teacher(left_img, right_img)
        student_output = student(left_img, right_img)

    print(f"✓ 前向传播成功")
    print(f"  教师输出形状: {teacher_output.shape}")
    print(f"  学生输出形状: {student_output.shape}")

    # 测试损失函数
    print("\n4. 测试损失函数...")
    from stereo_distillation.utils.losses import StereoLoss
    criterion = StereoLoss()
    loss = criterion(student_output, teacher_output, disparity)
    print(f"✓ 损失计算成功: {loss.item():.4f}")

    # 测试评估指标
    print("\n5. 测试评估指标...")
    from stereo_distillation.utils.metrics import compute_metrics
    metrics = compute_metrics(student_output, disparity)
    print(f"✓ 指标计算成功:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    print("\n" + "=" * 50)
    print("所有测试通过!")
    print("=" * 50)

if __name__ == "__main__":
    main()