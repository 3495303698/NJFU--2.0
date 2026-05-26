import torch

def compute_metrics(predicted, target):
    # Mean Absolute Error
    mae = torch.abs(predicted - target).mean().item()

    # Root Mean Square Error
    rmse = torch.sqrt(((predicted - target) ** 2).mean()).item()

    # Percentage of pixels with error < 3px
    error_map = torch.abs(predicted - target)
    d1 = (error_map < 3).float().mean().item()

    return {
        "MAE": mae,
        "RMSE": rmse,
        "D1": d1
    }