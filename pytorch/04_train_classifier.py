import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

torch.manual_seed(0)

# --- 1. Data ---
# Convert images to tensors and normalize pixel values to roughly [-1, 1]
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,)),
])

DATA_DIR = "C:/pytorch_data"  # short local path, avoids the UNC path entirely

train_data = datasets.FashionMNIST(DATA_DIR, train=True, download=True, transform=transform)
test_data = datasets.FashionMNIST(DATA_DIR, train=False, download=True, transform=transform)

CLASS_NAMES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

print(f"train samples: {len(train_data)}, test samples: {len(test_data)}")
print("one image shape:", train_data[0][0].shape)  # (1, 28, 28) -- 1 channel (grayscale)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=256, shuffle=False)

# --- 2. Model: a small CNN ---
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # Conv layers: slide small filters over the image to detect
        # edges/textures/shapes -- the standard approach for photos.
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)   # 1 -> 16 channels
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)  # 16 -> 32 channels
        self.pool = nn.MaxPool2d(2)  # halves height/width
        self.fc1 = nn.Linear(32 * 7 * 7, 64)
        self.fc2 = nn.Linear(64, 10)  # 10 output classes

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))   # 28x28 -> 14x14
        x = self.pool(F.relu(self.conv2(x)))   # 14x14 -> 7x7
        x = x.flatten(1)                        # flatten to (batch, 32*7*7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)                         # raw scores ("logits"), one per class
        return x

model = SimpleCNN()

# --- 3. Loss and optimizer ---
loss_fn = nn.CrossEntropyLoss()  # standard loss for multi-class classification
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# --- 4. Training loop ---
EPOCHS = 2  # keep small so it runs fast on CPU; accuracy improves with more

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()          # clear gradients from last step
        outputs = model(images)        # forward pass
        loss = loss_fn(outputs, labels)
        loss.backward()                # compute gradients
        optimizer.step()               # update weights
        total_loss += loss.item()
    avg_loss = total_loss / len(train_loader)
    print(f"epoch {epoch+1}/{EPOCHS} -- avg training loss: {avg_loss:.4f}")

# --- 5. Evaluate ---
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        predicted = outputs.argmax(dim=1)   # class with highest score
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

print(f"\ntest accuracy: {100 * correct / total:.2f}%")

# --- 6. Save the trained model so we can reuse it later (e.g. from a bot) ---
torch.save(model.state_dict(), "C:/pytorch_data/fashion_cnn.pt")
print("saved model to C:/pytorch_data/fashion_cnn.pt")
