# RGB values
colors = [
    (222, 239, 206),
    (222, 235, 198),
    (151, 154, 118),
    (137, 120, 101),
    (255, 51, 17),
    (115, 117, 132),
    (118, 121, 137)
]

# Create an image with the colors
from PIL import Image, ImageDraw

# Image size
width = 70 * len(colors)
height = 100
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Draw rectangles for each color
for i, color in enumerate(colors):
    x0 = i * 70
    y0 = 0
    x1 = x0 + 70
    y1 = 100
    draw.rectangle([x0, y0, x1, y1], fill=color)

# Save the image
image_path = "./color_swatches.png"
image.save(image_path)
image_path
