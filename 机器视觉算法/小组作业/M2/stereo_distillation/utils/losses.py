import torch
import torch.nn as nn

class StereoLoss(nn.Module):
    def __init__(self, alpha=0.7):
        super().__init__()
        self.alpha = alpha  # Weight for distillation vs ground truth
        self.l1_loss = nn.L1Loss()
        self.mse_loss = nn.MSELoss()

    def forward(self, student_output, teacher_output, ground_truth):
        # Distillation loss (student tries to match teacher)
        distill_loss = self.mse_loss(student_output, teacher_output)

        # Supervised loss (student tries to match ground truth)
        supervised_loss = self.l1_loss(student_output, ground_truth)

        # Combined loss
        total_loss = self.alpha * distill_loss + (1 - self.alpha) * supervised_loss

        return total_loss