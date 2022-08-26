from PIL import Image, ImageEnhance

def process(image):
    image = image.convert('L')
    enhancer = ImageEnhance.Contrast(image)
    factor = 1.8 
    im_output = enhancer.enhance(factor)
    return im_output


if __name__ == "__main__":
    image = Image.open("./bad.png")
    image = process(image)
    image.save("processed.jpg")
