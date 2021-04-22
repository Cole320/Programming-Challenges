# Dependency time
from PIL import Image, ImageOps

# Declaring constants
image = "image.png"
output = "output.txt"

original_image = ImageOps.grayscale(Image.open(image)) # open the original image and convert it to greyscale
original_image.show()

for