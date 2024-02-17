import matplotlib.pyplot as plt
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = plt.imread("a-27.jpg")
dx, dy = 48, 61
image = np.copy(img)
grid_color = [0, 0, 0]


if len(image.shape) == 3:
    image[:, ::dy, :] = grid_color
    image[::dx, :, :] = grid_color
    grid_locations = [(x, y) for x in range(0, image.shape[1], dy) for y in range(0, image.shape[0], dx)]
elif len(image.shape) == 2:  
    image[:, ::dy] = grid_color[0]
    image[::dx, :] = grid_color[0]
    grid_locations = [(x, y) for x in range(0, image.shape[1], dy) for y in range(0, image.shape[0], dx)]

# Extract text from each grid using Tesseract OCR
for x, y in grid_locations:
    grid = img[y:y + dy, x:x + dx]
    text = pytesseract.image_to_string(grid, config='--psm 6')
    # print(f"Text in grid at ({x}, {y}): {text.strip()}")

plt.imshow(image)
plt.scatter(*zip(*grid_locations), color='red', marker='.')
plt.show()
