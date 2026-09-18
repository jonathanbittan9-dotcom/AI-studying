import torch
import torch.nn as nn

# A network is a class that subclasses nn.Module.
# - __init__ declares the layers (each layer owns its own weights)
# - forward() defines how data flows through them
class TinyNet(nn.Module):
    def __init__(self, in_features, hidden, out_features):
        super().__init__()
        self.layer1 = nn.Linear(in_features, hidden)  # y = xW^T + b
        self.relu = nn.ReLU()                          # nonlinearity
        self.layer2 = nn.Linear(hidden, out_features)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

model = TinyNet(in_features=4, hidden=8, out_features=2)
print(model)

# Feed it a fake batch: 5 samples, each with 4 features
batch = torch.rand(5, 4)
output = model(batch)   # calls forward() under the hood
print("\ninput shape:", batch.shape)
print("output shape:", output.shape)   # (5, 2) — 2 raw scores per sample

# Inspect the learnable parameters PyTorch is tracking for you
print("\nParameters:")
for name, param in model.named_parameters():
    print(f"  {name}: shape {tuple(param.shape)}, requires_grad={param.requires_grad}")

total_params = sum(p.numel() for p in model.parameters())
print("\nTotal learnable numbers:", total_params)

# Why ReLU / nonlinearity matters:
# Without it, layer1 -> layer2 collapses mathematically into one big linear
# layer (stacking linear ops is still linear). ReLU lets the network learn
# curved, complex decision boundaries -- essential for real tasks like
# recognizing images.
