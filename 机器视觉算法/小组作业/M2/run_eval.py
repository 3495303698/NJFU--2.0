#!/usr/bin/env python
"""
立体匹配模型评估脚本
"""

import argparse
import torch
import os
from stereo_distillation.models.student import StudentModel
from stereo_distillation.data.dataloader import get_dataloader
from stereo_distillation.utils.metrics import compute_metrics

def main():
    parser = argparse.ArgumentParser(description="立体匹配模型评估")
    parser.add_argument("--model-path", type=str, required=True, help="模型路径")
    parser.add_argument("--batch-size", type=int, default=4, help="批次大小")

    args = parser.parse_args()

    print("=" * 50)
    print("立体匹配模型评估")
    print(f"模型: {args.model_path}")
    print("=" * 50)

    # 检查GPU可用性
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    # 检查模型文件是否存在
    if not os.path.exists(args.model_path):
        print(f"错误: 模型文件不存在: {args.model_path}")
        return

    # 初始化模型
    model = StudentModel().to(device)

    # 加载模型权重
    checkpoint = torch.load(args.model_path, map_location=device)
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)

    model.eval()
    print("模型加载成功!")

    # 数据加载器
    test_loader = get_dataloader(batch_size=args.batch_size, train=False)

    # 评估
    all_metrics = {"MAE": [], "RMSE": [], "D1": []}

    with torch.no_grad():
        for batch_idx, (left_img, right_img, disparity) in enumerate(test_loader):
            left_img = left_img.to(device)
            right_img = right_img.to(device)
            disparity = disparity.to(device)

            output = model(left_img, right_img)
            metrics = compute_metrics(output, disparity)

            for key in all_metrics.keys():
                all_metrics[key].append(metrics[key])

            if batch_idx % 5 == 0:
                print(f"处理批次 {batch_idx}/{len(test_loader)}")

    # 计算平均指标
    print("\n评估结果:")
    print("-" * 30)
    for key, values in all_metrics.items():
        avg_value = sum(values) / len(values)
        print(f"{key}: {avg_value:.4f}")

    print("=" * 50)
    print("评估完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()