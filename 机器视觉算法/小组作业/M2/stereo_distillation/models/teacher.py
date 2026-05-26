import torch
import torch.nn as nn

class TeacherModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Simple CNN for demonstration
        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 1, 3, padding=1),
        )

    def forward(self, left_img, right_img):
        # Simple feature extraction and disparity estimation
        left_features = self.conv(left_img)
        right_features = self.conv(right_img)

        # Simple correlation-based disparity (for demo purposes)
        batch_size, _, h, w = left_features.shape
        disparity = torch.zeros(batch_size, h, w)

        # This is a simplified version - real implementations would use more sophisticated methods
        for b in range(batch_size):
            for i in range(h):
                for j in range(w):
                    # Find best match in right image (simplified)
                    best_match = 0
                    min_diff = float('inf')
                    for d in range(min(64, w - j)):
                        diff = torch.abs(left_features[b, :, i, j] - right_features[b, :, i, j + d]).mean()
                        if diff < min_diff:
                            min_diff = diff
                            best_match = d
                    disparity[b, i, j] = best_match

        return disparity.unsqueeze(1)
