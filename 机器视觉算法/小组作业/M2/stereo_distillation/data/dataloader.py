import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class SyntheticStereoDataset(Dataset):
    def __init__(self, size=100, image_size=(64, 64), train=True):
        self.size = size
        self.image_size = image_size
        self.train = train

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        # Generate synthetic stereo images and disparity
        h, w = self.image_size

        # Create random texture
        left_img = torch.randn(3, h, w)

        # Create right image by shifting pixels (simulating disparity)
        disparity = torch.randint(0, 10, (h, w)).float() / 10.0

        right_img = torch.zeros_like(left_img)
        for i in range(h):
            for j in range(w):
                shift = int(disparity[i, j] * 5)  # Scale disparity
                new_j = max(0, min(w-1, j + shift))
                right_img[:, i, j] = left_img[:, i, new_j]

        # Add some noise to make it more realistic
        right_img += torch.randn_like(right_img) * 0.1

        return left_img, right_img, disparity.unsqueeze(0)

def get_dataloader(batch_size=4, train=True):
    dataset = SyntheticStereoDataset(train=train)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=train)
    return dataloader