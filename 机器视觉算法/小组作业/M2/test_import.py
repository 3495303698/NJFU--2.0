import torch
from stereo_distillation.models.teacher import TeacherModel
from stereo_distillation.models.student import StudentModel
from stereo_distillation.data.dataloader import get_dataloader
from stereo_distillation.utils.losses import StereoLoss

print("测试训练流程...")

# 初始化组件
teacher = TeacherModel()
student = StudentModel()
dataloader = get_dataloader(batch_size=2)
criterion = StereoLoss()
optimizer = torch.optim.Adam(student.parameters(), lr=0.001)

# 一个训练步骤
for batch_idx, (left_img, right_img, disparity) in enumerate(dataloader):
    print(f"训练批次 {batch_idx}")

    # 前向传播
    with torch.no_grad():
        teacher_output = teacher(left_img, right_img)
    student_output = student(left_img, right_img)

    # 计算损失
    loss = criterion(student_output, teacher_output, disparity)
    print(f"  损失: {loss.item():.4f}")

    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if batch_idx == 2:  # 只测试几个批次
        break

print("训练流程测试通过！")