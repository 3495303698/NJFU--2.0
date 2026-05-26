import torch
import torch.nn as nn

class StudentModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Simplified version of teacher for distillation
        self.conv = nn.Sequential(
            nn.Conv2d(3, 8, 3, padding=1),  # Fewer filters than teacher
            nn.ReLU(),
            nn.Conv2d(8, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 1, 3, padding=1),
        )

    def forward(self, left_img, right_img):
        # Simple forward pass - in practice, this would implement a real stereo matching algorithm
        left_features = self.conv(left_img)
        right_features = self.conv(right_img)

        # Simple disparity computation (for demo)
        disparity = torch.abs(left_features - right_features).mean(dim=1, keepdim=True) * 10
        return disparity
