import argparse
import torch
from stereo_distillation.models.student import StudentModel
from stereo_distillation.data.dataloader import get_dataloader
from stereo_distillation.utils.metrics import compute_metrics

def main():
    parser = argparse.ArgumentParser(description="Evaluate stereo matching model")
    parser.add_argument("--model-path", type=str, required=True, help="Path to trained model")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")

    args = parser.parse_args()

    print(f"Starting evaluation with model: {args.model_path}")

    # Initialize model
    model = StudentModel()
    model.load_state_dict(torch.load(args.model_path))
    model.eval()

    # Get dataloader
    dataloader = get_dataloader(batch_size=args.batch_size, train=False)

    # Evaluation loop
    all_metrics = {}
    with torch.no_grad():
        for left_img, right_img, disparity in dataloader:
            output = model(left_img, right_img)
            metrics = compute_metrics(output, disparity)

            # Aggregate metrics
            for key, value in metrics.items():
                if key not in all_metrics:
                    all_metrics[key] = []
                all_metrics[key].append(value)

    # Print average metrics
    print("Evaluation Results:")
    for key, values in all_metrics.items():
        avg_value = sum(values) / len(values)
        print(f"{key}: {avg_value:.4f}")

if __name__ == "__main__":
    main()