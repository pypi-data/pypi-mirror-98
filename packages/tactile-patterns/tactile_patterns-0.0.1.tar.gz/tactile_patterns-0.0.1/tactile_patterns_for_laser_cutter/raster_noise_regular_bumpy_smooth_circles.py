import numpy as np
import math
from PIL import Image

def squared_distance_from_circle_to_value(squared_distance):
    scaled_distance =  math.sqrt(squared_distance) * 3
    scaled = 255 - scaled_distance
    if scaled < 0:
        return 0
    return int(scaled)

def squared_distance_from_center(x, y):
    x = x % 240
    y = y % 240
    center_x = 120
    center_y = 120
    delta_x = x - center_x
    delta_y = y - center_y
    return delta_x * delta_x + delta_y * delta_y

def value_for_location(x, y):
    squared_distance = squared_distance_from_center(x, y)
    return squared_distance_from_circle_to_value(squared_distance)

size = 1000
width = size
height = size

# https://pillow.readthedocs.io/en/latest/reference/Image.html
im = Image.new("RGB", (width, height), (255, 0, 0))
pixels = im.load()
for x in range(0, width):
    for y in range(0, height):
        value = value_for_location(x, y)
        pixels[x, y] = (value, value, value)
im.save("generated.png")
im.show()
