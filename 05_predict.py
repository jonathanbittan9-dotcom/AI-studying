import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from torchvision.datasets import FashionMNIST

CLASS_NAMES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# Same architecture as training -- must match exactly to load the saved weights
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(32 * 7 * 7, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.flatten(1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def load_model(path="C:/pytorch_data/fashion_cnn.pt"):
    model = SimpleCNN()
    model.load_state_dict(torch.load(path, map_location="cpu"))
    model.eval()   # inference mode: disables things like dropout
    return model


def predict(model, image_tensor):
    """
    image_tensor: shape (1, 28, 28), pixel values already normalized
    like at training time. Returns (label, confidence).

    This is the shape of function a Discord bot command handler would call:
        - user uploads a photo
        - you preprocess it into a tensor (resize, normalize)
        - call predict()
        - reply with the label
    """
    with torch.no_grad():                       # no need to track gradients for inference
        batch = image_tensor.unsqueeze(0)        # add batch dimension: (1, 1, 28, 28)
        logits = model(batch)
        probs = F.softmax(logits, dim=1)         # convert raw scores -> probabilities
        confidence, predicted_idx = probs.max(dim=1)
    return CLASS_NAMES[predicted_idx.item()], confidence.item()


if __name__ == "__main__":
    model = load_model()

    # Grab a few real test images to simulate "photos a user sent"
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ])
    test_data = FashionMNIST("C:/pytorch_data", train=False, download=True, transform=transform)

    for i in [0, 1, 2, 3, 4]:
        image, true_label = test_data[i]
        predicted_label, confidence = predict(model, image)
        correct = "OK" if predicted_label == CLASS_NAMES[true_label] else "WRONG"
        print(f"true: {CLASS_NAMES[true_label]:15s} | "
              f"predicted: {predicted_label:15s} ({confidence*100:.1f}% confident) {correct}")
