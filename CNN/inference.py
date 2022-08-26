import torch
import torchvision.transforms as transforms
from PIL import Image
import os

transform = transforms.Compose(
    [transforms.Resize((600, 600)),  
     transforms.ToTensor(),   
     transforms.Normalize((0.5), (0.5))])


classes = ("Factura", "Oplata", "Invalid")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_NAME = "./checkpoints/epoch_12.t"
CHECK_DIR = "./Dataset/check"
model = torch.load(MODEL_NAME)
model.to(device)
check_files = os.listdir(CHECK_DIR)
print(check_files)
for image_path in check_files:
    image = Image.open(f"{CHECK_DIR}/{image_path}")
    tensor = transform(image).unsqueeze(0)
    outputs = model(tensor.to(device))
    _, predicted = torch.max(outputs, 1)
    print(image_path, classes[predicted])


