#!/usr/bin/env python
"""
立体匹配蒸馏训练脚本
"""

import argparse
import torch
import os
import time
from stereo_distillation.models.teacher import TeacherModel
from stereo_distillation.models.student import StudentModel
from stereo_distillation.data.dataloader import get_dataloader
from stereo_distillation.utils.losses import StereoLoss
from stereo_distillation.utils.metrics import compute_metrics

def main():
    parser = argparse.ArgumentParser(description="立体匹配蒸馏训练")
    parser.add_argument("--epochs", type=int, default=5, help="训练轮数")
    parser.add_argument("--batch-size", type=int, default=2, help="批次大小")
    parser.add_argument("--lr", type=float, default=1e-3, help="学习率")
    parser.add_argument("--save-dir", type=str, default="checkpoints", help="模型保存目录")
    parser.add_argument("--log-interval", type=int, default=5, help="日志打印间隔")

    args = parser.parse_args()

    # 创建保存目录
    os.makedirs(args.save_dir, exist_ok=True)

    print("=" * 50)
    print("立体匹配蒸馏训练开始")
    print(f"参数: {args}")
    print("=" * 50)

    # 检查GPU可用性
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    # 初始化模型
    teacher = TeacherModel().to(device)
    student = StudentModel().to(device)

    print(f"教师模型参数量: {sum(p.numel() for p in teacher.parameters())}")
    print(f"学生模型参数量: {sum(p.numel() for p in student.parameters())}")

    # 数据加载器
    train_loader = get_dataloader(batch_size=args.batch_size, train=True)
    val_loader = get_dataloader(batch_size=args.batch_size, train=False)

    print(f"训练批次: {len(train_loader)}, 验证批次: {len(val_loader)}")

    # 优化器和损失函数
    optimizer = torch.optim.Adam(student.parameters(), lr=args.lr)
    criterion = StereoLoss()

    # 训练循环
    for epoch in range(args.epochs):
        print(f"\n--- Epoch {epoch+1}/{args.epochs} ---")
        start_time = time.time()

        # 训练阶段
        student.train()
        train_loss = 0.0
        train_batches = 0

        for batch_idx, (left_img, right_img, disparity) in enumerate(train_loader):
            left_img = left_img.to(device)
            right_img = right_img.to(device)
            disparity = disparity.to(device)

            # 前向传播
            with torch.no_grad():
                teacher_output = teacher(left_img, right_img)
            student_output = student(left_img, right_img)

            # 计算损失
            loss = criterion(student_output, teacher_output, disparity)
            train_loss += loss.item()
            train_batches += 1

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch_idx % args.log_interval == 0:
                print(f"  批次 {batch_idx}/{len(train_loader)}, 损失: {loss.item():.4f}")

        # 验证阶段
        student.eval()
        val_metrics = {"MAE": [], "RMSE": [], "D1": []}

        with torch.no_grad():
            for left_img, right_img, disparity in val_loader:
                left_img = left_img.to(device)
                right_img = right_img.to(device)
                disparity = disparity.to(device)

                student_output = student(left_img, right_img)
                metrics = compute_metrics(student_output, disparity)

                for key in val_metrics.keys():
                    val_metrics[key].append(metrics[key])

        # 计算平均值
        avg_train_loss = train_loss / train_batches
        epoch_time = time.time() - start_time

        print(f"Epoch {epoch+1} 完成 (耗时: {epoch_time:.2f}s):")
        print(f"  训练损失: {avg_train_loss:.4f}")
        for key, values in val_metrics.items():
            avg_value = sum(values) / len(values)
            print(f"  验证 {key}: {avg_value:.4f}")

        # 保存模型
        if (epoch + 1) % 2 == 0 or epoch == args.epochs - 1:
            model_path = os.path.join(args.save_dir, f"student_epoch_{epoch+1}.pth")
            torch.save({
                'epoch': epoch,
                'model_state_dict': student.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': avg_train_loss,
            }, model_path)
            print(f"  模型已保存: {model_path}")

    print("\n" + "=" * 50)
    print("训练完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()