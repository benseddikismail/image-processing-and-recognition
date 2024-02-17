# Import the Image and ImageFilter classes from PIL (Pillow)
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from skimage import measure
from skimage.draw import rectangle_perimeter


# In this method we preprocess the image to perform noise reduction
def image_preprocessing(img):
    # Applying mean filtering from Pillow
    box = [1] * 25
    result = img.filter(ImageFilter.Kernel((5, 5), box, sum(box)))
    result.save("preprocessed_img.png")
    return result


def detect_contours(image_array):
    threshold = 40
    binary_image = image_array > threshold

    inverted_binary_image = np.invert(binary_image)
    labeled_image = measure.label(inverted_binary_image, connectivity=2)

    contours = measure.find_contours(labeled_image, 0.5)
    filtered_contours = []
    for contour in contours:
        min_row, min_col, max_row, max_col = (
            np.min(contour[:, 0]),
            np.min(contour[:, 1]),
            np.max(contour[:, 0]),
            np.max(contour[:, 1]),
        )

        aspect_ratio = (max_row - min_row) / (max_col - min_col)

        if 0.7 < aspect_ratio < 1.3:
            filled_area_mask = np.zeros_like(inverted_binary_image, dtype=np.uint8)
            filled_area_mask[
                int(min_row) : int(max_row), int(min_col) : int(max_col)
            ] = 1
            filled_area = np.sum(filled_area_mask)
            bounding_box_area = (max_row - min_row) * (max_col - min_col)
            if 0.2 < filled_area / bounding_box_area < 1.2:
                filtered_contours.append(contour)

    return filtered_contours


def draw_contours(image, contours):
    image_rgb = image.convert("RGB")
    draw = ImageDraw.Draw(image_rgb)

    for contour in contours:
        threshold_sum = 50000
        contour = np.round(contour).astype(int)

        # Calculate the sum of pixel values within the contour
        contour_sum = np.sum(
            image_rgb.crop(
                [
                    min(contour[:, 1]),
                    min(contour[:, 0]),
                    max(contour[:, 1]),
                    max(contour[:, 0]),
                ]
            ).convert("L")
        )

        if contour_sum < threshold_sum:
            draw.line(
                list(zip(contour[:, 1], contour[:, 0])), fill=(0, 0, 255), width=10
            )

    return image_rgb


if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise Exception(
            "error: please give an input image name as a parameter, like this: \n"
            "python3 pichu_devil.py input.jpg"
        )

    # Load an image
    im = Image.open(sys.argv[1])

    # Check its width, height, and number of color channels
    print("Image is %s pixels wide." % im.width)
    print("Image is %s pixels high." % im.height)
    print("Image mode is %s." % im.mode)

    # Pixels are accessed via an (X,Y) tuple.
    # The coordinate system starts at (0,0) in the upper left-hand corner,
    # and increases moving right (first coordinate) and down (second coordinate).
    # So it's a (col, row) indexing system, not (row, col) like we're used to
    # when dealing with matrices or 2d arrays.
    print("Pixel value at (10,10) is %s" % str(im.getpixel((10, 10))))

    # Pixels can be modified by specifying the coordinate and RGB value
    # (255, 0, 0) is a pure red pixel.
    im.putpixel((10, 10), 255)
    print("New pixel value is %s" % str(im.getpixel((10, 10))))

    # Let's create a grayscale version of the image:
    # the "L" means there's only a single channel, "Lightness"
    gray_im = im.convert("L")

    # Create a new blank color image the same size as the input
    color_im = Image.new("RGB", (im.width, im.height), color=0)
    gray_im.save("gray.png")

    """
    # Highlights any very dark areas with red.
    for x in range(im.width):
        for y in range(im.height):
            p = gray_im.getpixel((x, y))
            if p < 50:
                (R, G, B) = (255, 0, 0)
                color_im.putpixel((x, y), (R, G, B))
            else:
                color_im.putpixel((x, y), (p, p, p))

    # Show the image. We're commenting this out because it won't work on the Linux
    # server (unless you set up an X Window server or remote desktop) and may not
    # work by default on your local machine. But you may want to try uncommenting it,
    # as seeing results in real-time can be very useful for debugging!
    #    color_im.show()

    # Save the image
    color_im.save("output.png")

    # This uses Pillow's code to create a 5x5 mean filter and apply it to
    # our image.
    # Since the input is a color image, Pillow applies the filter to each
    # of the three color planes (R, G, and B) independently.
    box = [1] * 25
    result = color_im.filter(ImageFilter.Kernel((5, 5), box, sum(box)))
    # result.show()
    result.save("output2.png")
    """
    # Image preprocessing
    preprocessed_im = image_preprocessing(gray_im)

    image_array = np.array(preprocessed_im)
    # Detect contours
    contours = detect_contours(image_array)

    # Draw contours on the original image
    image_with_contours = Image.open(sys.argv[1])
    image_with_contours = draw_contours(image_with_contours, contours)

    # Display or save the result
    image_with_contours.show()
    image_with_contours.save("OMR_with_contour.jpg")
