import torch
import sys

def inspect_checkpoint(checkpoint_path):
    # Load the checkpoint
    try:
        checkpoint = torch.load(checkpoint_path)
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        sys.exit(1)

    # Print the keys in the checkpoint
    print("Checkpoint keys:")
    for key in checkpoint.keys():
        print(key)

    # Print details of model state_dict
    if 'model_state_dict' in checkpoint:
        print("\nModel State Dict:")
        for param_tensor in checkpoint['model_state_dict']:
            print(param_tensor, "\t", checkpoint['model_state_dict'][param_tensor].size())

    # Print details of optimizer state_dict
    if 'optimizer_state_dict' in checkpoint:
        print("\nOptimizer State Dict:")
        for param_tensor in checkpoint['optimizer_state_dict']:
            print(param_tensor, "\t", checkpoint['optimizer_state_dict'][param_tensor].size())

    # Print epoch and loss if available
    print("\nEpoch:", checkpoint.get('epoch', 'Not found'))
    print("Loss:", checkpoint.get('loss', 'Not found'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_checkpoint.py <path_to_checkpoint>")
        sys.exit(1)

    checkpoint_path = sys.argv[1]
    inspect_checkpoint(checkpoint_path)