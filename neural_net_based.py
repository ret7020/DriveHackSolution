import torch
import torchvision.transforms as transforms
from PIL import Image
import time

class Segmentator:
    def __init__(self, model_path):
        self.model = torch.load(model_path)
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.model.to(self.device)
        self.transform = transforms.Compose(
                [transforms.Resize((600, 600)),  
                transforms.ToTensor(),   
                transforms.Normalize((0.5), (0.5))]
            )
        self.classes = ("Factura", "Oplata")
    def recognize(self, image):
        tensor = self.transform(image).unsqueeze(0)
        outputs = self.model(tensor.to(self.device))
        _, predicted = torch.max(outputs, 1)
        return predicted

if __name__ == "__main__":
    print("Testing NN")
    net = Segmentator("./Server/epoch_12.t")
    ts = time.time()
    image = Image.open("../Dataset/check/factura.jpg")
    print(time.time() - ts)
    print(net.recognize(image))
    print("Model loaded")


