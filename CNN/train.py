import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import numpy as np
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def image_shower(images, labels, n=4):
    plt.figure(figsize=(12, 12))
    for i, image in enumerate(images[:n]):
        plt.subplot(n, n, i + 1)
        image = image/ 2 + 0.5
        plt.imshow(image.numpy().transpose((1, 2, 0)).squeeze())
    print("Real Labels: ", ' '.join('%5s' % classes[label] for label in labels[:n]))
classes = ("Factura", "Oplata", "Invalid")

PATH = "./Dataset"
transform = transforms.Compose(
    [transforms.Resize((600, 600)), 
     transforms.ToTensor(),
     transforms.Normalize((0.5), (0.5))]) 


trainset = torchvision.datasets.ImageFolder(os.path.join(PATH, "train"), transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=5, num_workers=0, shuffle=True)

testset = torchvision.datasets.ImageFolder(os.path.join(PATH, "test"), transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=5, num_workers=0, shuffle=True)

images, labels = next(iter(trainloader))

#model = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained=True)
model = torch.hub.load('pytorch/vision:v0.10.0', 'vgg16', pretrained=True)
for param in model.parameters():
    param.require = False

model.fc = nn.Linear(2048, 4)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr = 0.00001, momentum=0.9)
epochs = 30
model.to(device)


torch.cuda.empty_cache()

for epoch in range(epochs):
    running_loss = 0.0
    for i, data in tqdm(enumerate(trainloader)):
        inputs, labels = data[0].to(device), data[1].to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    torch.save(model, f"./checkpoints/epoch_{epoch}.t")
    print ("Epoch {} - Training loss: {} ".format(epoch, running_loss/len(trainloader)))

torch.save("./checkpoints/final.t")

