import numpy as np
from PIL import Image

multiplier = 3
width = 255 * multiplier
height = 100

# https://pillow.readthedocs.io/en/latest/reference/Image.html
im = Image.new("RGB", (width, height), (255, 0, 0))
pixels = im.load()
for x in range(0, width):
    for y in range(0, height):
        value = int(255.0 * x / width)
        pixels[x, y] = (value, value, value)
im.save("generated.png")
im.show()
