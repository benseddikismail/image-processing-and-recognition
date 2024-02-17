import matplotlib.pyplot as plt
from skimage import io, color
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
import matplotlib.image as img


image_path = "a-27.jpg"
image = io.imread(image_path)


if len(image.shape) == 3:
    gray_image = color.rgb2gray(image)
else:
    gray_image = image

thresh = threshold_otsu(gray_image)
binary_image = gray_image > thresh


cleaned_image = closing(binary_image, square(3))
cleaned_image = clear_border(cleaned_image)
label_image = label(cleaned_image)


figure, axes = plt.subplots(figsize=(8, 8))
axes.imshow(label2rgb(label_image, image=image, bg_label=0), cmap='gray')

c=0
for reg in regionprops(label_image):
    minr, minc, maxr, maxc = reg.bbox
    print(minc, minr, maxc-minc, maxr-minr)
    c+=1
    rect = plt.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=2)
    axes.add_patch(rect)


print(c)
plt.title('Segmented Image with Bounding Boxes')
plt.show()