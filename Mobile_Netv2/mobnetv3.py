# -*- coding: utf-8 -*-
"""mobnetv3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bjDwGqO2l01BOUkdgfabduyVZhQe2sV3
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models
import matplotlib.pyplot as plt

""" Set device (GPU if available, else CPU)

"""

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

"""Load CIFAR-100 dataset"""

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize inputs
])

trainset = torchvision.datasets.CIFAR100(root='./data', train=True, download=True, transform=transform)
train_size = int(0.8 * len(trainset))
val_size = len(trainset) - train_size

trainset, valset = torch.utils.data.random_split(trainset, [train_size, val_size])

trainloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True, num_workers=2)
valloader = torch.utils.data.DataLoader(valset, batch_size=32, shuffle=False, num_workers=2)

testset = torchvision.datasets.CIFAR100(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=32, shuffle=False, num_workers=2)

"""Define your model architecture (MobileNetV3)"""

model = models.mobilenet_v3_small(pretrained=True)
num_ftrs = model.classifier[3].in_features
model.classifier[3] = nn.Linear(num_ftrs, 100)  # Modify the final fully connected layer for 100 classes

"""Move model to device"""

model = model.to(device)

"""Define loss function and optimizer"""

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

"""Fine-tuning and training"""

num_epochs = 10

"""Lists to store validation and test accuracies"""

val_accs = []
test_accs = []

for epoch in range(num_epochs):
    # Training
    model.train()
    train_loss = 0.0

    for inputs, labels in trainloader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item() * inputs.size(0)

    # Validation
    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for inputs, labels in valloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_accuracy = 100.0 * val_correct / val_total
    val_accs.append(val_accuracy)

    # Testing
    test_correct = 0
    test_total = 0

    with torch.no_grad():
        for inputs, labels in testloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            test_total += labels.size(0)
            test_correct += (predicted == labels).sum().item()

    test_accuracy = 100.0 * test_correct / test_total
    test_accs.append(test_accuracy)

    print(f'Epoch {epoch+1}/{num_epochs}: Train Loss: {train_loss/len(trainset):.4f}, '
          f'Val Accuracy: {val_accuracy:.2f}%, Test Accuracy: {test_accuracy:.2f}%')

"""# Plot epoch vs validation accuracy graph

"""

# Plot epoch vs validation accuracy graph
plt.plot(range(1, num_epochs+1), val_accs)
plt.xlabel('Epoch')
plt.ylabel('Validation Accuracy')
plt.title('Epoch vs Validation Accuracy')
plt.show()

"""# Plot epoch vs test accuracy graph"""

plt.plot(range(1, num_epochs+1), test_accs)
plt.xlabel('Epoch')
plt.ylabel('Test Accuracy')
plt.title('Epoch vs Test Accuracy')
plt.show()