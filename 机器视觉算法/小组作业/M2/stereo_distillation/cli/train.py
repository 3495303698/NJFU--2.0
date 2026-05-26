import argparse
import torch
from stereo_distillation.models.teacher import TeacherModel
from stereo_distillation.models.student import StudentModel
from stereo_distillation.data.dataloader import get_dataloader
from stereo_distillation.utils.losses import StereoLoss

def main():
    parser = argparse.ArgumentParser(description="Train stereo matching model")
    parser.add_argument("--config", type=str, default="configs/default.yaml", help="Config file")
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")

    args = parser.parse_args()

    print(f"Starting training with args: {args}")

    # Initialize models
    teacher = TeacherModel()
    student = StudentModel()

    # Get dataloader
    dataloader = get_dataloader(batch_size=args.batch_size)

    # Loss and optimizer
    criterion = StereoLoss()
    optimizer = torch.optim.Adam(student.parameters(), lr=args.lr)

    # Training loop (simplified)
    for epoch in range(args.epochs):
        for batch_idx, (left_img, right_img, disparity) in enumerate(dataloader):
            # Forward pass
            with torch.no_grad():
                teacher_output = teacher(left_img, right_img)
            student_output = student(left_img, right_img)

            # Compute loss
            loss = criterion(student_output, teacher_output, disparity)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch_idx % 10 == 0:
                print(f"Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item():.4f}")

    print("Training completed!")

if __name__ == "__main__":
    main()