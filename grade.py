#Import the Image and ImageFilter classes from PIL (Pillow)
from PIL import Image
from PIL import ImageFilter
import sys
import random
import numpy as np

# import matplotlib.pyplot as plt


def preprocess(image, edges_arr):

    img_arr = np.asarray(image)

    # thresholding
    processed_img = np.zeros(img_arr.shape, dtype=float)
    processed_img[img_arr < 5] = 255 
    #plt.imshow(img_arr)
    #plt.show()

    vertical_regions, horizontal_regions = edges_arr.copy(), edges_arr.copy()
    
    # identify horizontal and vertical question regions 
    for c in range(vertical_regions.shape[0]):
        if np.sum(vertical_regions[c,:] > 10) > 150:
            vertical_regions[c,:] = 255
    for r in range(horizontal_regions.shape[1]):
        if np.sum(horizontal_regions[:,r] > 10) > 200: #
            horizontal_regions[:,r] = 255    
    # dilation
    horizontal_regions = Image.fromarray(np.uint8(horizontal_regions), mode="L").filter(ImageFilter.MinFilter(3))
    vertical_regions = Image.fromarray(np.uint8(vertical_regions), mode="L").filter(ImageFilter.MinFilter(3))
    # erosion
    horizontal_regions = horizontal_regions.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MaxFilter(3))
    vertical_regions = vertical_regions.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MaxFilter(3))
    # plt.figure(figsize=(8, 8))
    # plt.subplot(1, 2, 1)
    # plt.imshow(vertical_regions, cmap='gray')
    # plt.title('Vertical Regions')
    # plt.subplot(1, 2, 2)
    # plt.imshow(horizontal_regions, cmap='gray')
    # plt.title('Horizontal Regions')
    # plt.show()

    # identify answer boxes
    crossing = (np.asarray(horizontal_regions) == 255) * (np.asarray(vertical_regions) == 255)
    # min filters to remove noise 
    boxes_img = Image.fromarray(np.uint8(crossing * 255)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MinFilter(7))
    answer_boxes = np.array(boxes_img)[600:]

    return answer_boxes, processed_img

def detect_regions(image):

    # edge detection
    edges = image.filter(ImageFilter.FIND_EDGES)
    edges_arr = np.asarray(edges)

    answer_boxes, processed_img = preprocess(image, edges_arr)

    region_found = False
    for col in range(0, answer_boxes.shape[1]):
        for row in range(0, answer_boxes.shape[0]):
            if answer_boxes[row, col] == 255:
                region_found = True
                start_pos = (row, col)
                break
        if region_found:
            break

    coordinates = list()
    region_start, current, n_pixels = False, None, 50
    for column_index in range(start_pos[1], answer_boxes.shape[1]):
        if answer_boxes[start_pos[0], column_index] == 255:
            n_pixels = 50
            current = (start_pos[0], column_index)
            if region_start:
                coordinates.append(current)
                region_start = False
        else:
            n_pixels -= 1
        if n_pixels == 0:
            coordinates.append(current)
            n_pixels = 50
            region_start = True

    y_coordinates = sorted(np.array(list(set(coordinates)))[:, 1])

    x = []
    found, counter = False, 28
    x.append(start_pos[0] + 595)
    for row in range(start_pos[0], answer_boxes.shape[0]):
        if counter == 0:
            break
        if answer_boxes[row, start_pos[1]] == 255:
            if found:
                x.append(row + 595)
                counter -= 1
                found = False
        else:
            found = True

    column1 = (start_pos[1] - 55, y_coordinates[0] + 40)
    column2 = (y_coordinates[1] - 55, y_coordinates[2] + 40)
    column3 = (y_coordinates[3] - 55, y_coordinates[4] + 40)
    if len(y_coordinates) < 5: 
        column1 = (165, 575)
        column2 = (598, 1007)
        column3 = (1029, 1443)
    # plt.imshow(answer_boxes, cmap='gray')
    # plt.axvline(x=column1[0], color='red', linestyle='--', linewidth=1)
    # plt.axvline(x=column1[1], color='red', linestyle='--', linewidth=1)
    # plt.axvline(x=column2[0], color='blue', linestyle='--', linewidth=1)
    # plt.axvline(x=column2[1], color='blue', linestyle='--', linewidth=1)
    # plt.axvline(x=column3[0], color='green', linestyle='--', linewidth=1)
    # plt.axvline(x=column3[1], color='green', linestyle='--', linewidth=1)
    # plt.show()

    region1_edges = edges_arr[:,column1[0]:column1[1]].astype(float)
    region1_im = processed_img[:,column1[0]:column1[1]].astype(float)
    region1 = (region1_edges, region1_im)
    region2_edges = edges_arr[:,column2[0]:column2[1]].astype(float)
    region2_im = processed_img[:,column2[0]:column2[1]].astype(float)
    region2 = (region2_edges, region2_im)
    region3_edges = edges_arr[:,column3[0]:column3[1]].astype(float)
    region3_im = processed_img[:,column3[0]:column3[1]].astype(float)
    region3 = (region3_edges, region3_im)

    return region1, region2, region3, x


def extract_segments(question):
    filter = np.ones((question.shape[0], 1))
    for i in range(question.shape[1]):
        if i == question.shape[1] - filter.shape[1] + 1:
            break
        product = filter * question[:, i:i + filter.shape[1]]
        if np.sum(np.sum(product == 255, axis=0) > 0):
            question[:, i] = 255

    processed_question = Image.fromarray(np.uint8(question), mode='L').filter(ImageFilter.MinFilter(3))
    processed_question = processed_question.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MaxFilter(3))
    return np.asarray(processed_question)

def process_segments(segments, current_img):
    answers = {0: 'x', 1: "", 2: "A", 3: "B", 4: "C", 5: "D", 6: "E"}
    del_cnt, counter, answer_str = 0, 6, ""
    for _, blob in enumerate(segments[::-1]):
        if (np.sum(current_img[:, blob[0]:blob[1]] == 255)) < 50:
            del_cnt += 1
            continue
        else:
            if np.sum(current_img[:, blob[0]:blob[1]]) > 120000 and counter >= 0:
                answer_str += answers[counter]
        counter -= 1
    answer_str = answer_str[::-1]
    if len(segments) - del_cnt >= 7:  # multiple answer choice
        answer_str = answer_str + " " + answers[0]
    return answer_str.strip()

def extract_answers(region_tuple, N_questions, coordinates):
    answer = []
    max_questions = 29
    region, img = region_tuple
    if len(coordinates) < max_questions:
        coordinates = np.arange(675, len(region), 47)
        step_size = 47
    else:
        step_size = 47

    for x in coordinates:
        question = region[x:x + step_size, :].copy()
        current_img = img[x:x + step_size, :].copy()
        if question.shape[0] < step_size or np.sum(current_img) == 0:
            continue

        dilation_arr = extract_segments(question)

        segments = []
        found = True
        for i in range(dilation_arr.shape[1]):
            if np.sum(dilation_arr[:, i] == 255) == step_size and found:
                start_pixel = i
                found = False
            elif np.sum(dilation_arr[:, i] == 255) < step_size and found != True:
                end_pixel = i
                found = True
                segments.append([start_pixel, end_pixel])

        answer_str = process_segments(segments, current_img)

        if N_questions == 0:
            break
        answer.append(answer_str)
        N_questions -= 1

    return answer

            
if __name__ == "__main__":

    if(len(sys.argv) < 3):
        raise Exception("Usage: python3 grade.py <input_image> <answer_str_text>")
    else:
        image_path = sys.argv[1]
        output_file = sys.argv[2]

    im = Image.open(image_path)
    im = im.convert("L")

    region1, region2, region3, x_coordinates = detect_regions(im)

    # Check its width, height, and number of color channels
    print("Image is %s pixels wide." % im.width)
    print("Image is %s pixels high." % im.height)
    print("Image mode is %s." % im.mode)

    with open(str(output_file), "w") as file:
        # extract answers from each region and write to file
        for i, answer in enumerate(
            extract_answers(region1, 29, x_coordinates)
            + extract_answers(region2, 29, x_coordinates)
            + extract_answers(region3, 27, x_coordinates)
        ):
            file.write(f"{i+1} {answer}\n")
