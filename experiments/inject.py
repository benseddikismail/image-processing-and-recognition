from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def correct_bubble(image, que_num, ans_letter, col_starts, x_dist, y_dist, size_bubble):
    # new_size = (2000,2000)
    # image = img.resize(new_size)
    offset = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    col = (que_num - 1) // 29
    row = (que_num - 1) % 29

    start_position = col_starts[col]
    pos_x = start_position[0] + offset[ans_letter] * x_dist
    pos_y = start_position[1] + row * y_dist
    draw = ImageDraw.Draw(image)
    draw.rectangle([pos_x, pos_y, pos_x + size_bubble, pos_y + size_bubble], fill="black")

omr_sheet_path = 'blank_form.jpg'  
omr_sheet = Image.open(omr_sheet_path)

x_pix_start = 275
y_pix_start = 655
x_dist = 52  
y_dist = 50  
size_bubble = 38  

column_gap = 230 
column_width = 4 * x_dist 
col_starts = {
    0: (x_pix_start, y_pix_start),
    1: (x_pix_start + column_width + column_gap, y_pix_start),
    2: (x_pix_start + 2 * (column_width + column_gap), y_pix_start)
}

ans_1 = {}  
ans_2 = {}  
answers = {}   

# with open('a-27_groundtruth.txt', 'r') as file:
with open('a-3_groundtruth.txt', 'r') as file:
    for line in file:
        parts = line.split()
        que_num = int(parts[0])
        ans = parts[1]
        if len(ans) > 1:
            ans_1[que_num] = ans[0]  
            ans_2[que_num] = ans[1]  
        else:
            answers[que_num] = ans


# print(answers)
for que_number, ans_letter in answers.items():
    correct_bubble(omr_sheet, que_number, ans_letter, col_starts, x_dist, y_dist, size_bubble)
    
for que_number, ans_letter in ans_1.items():
    correct_bubble(omr_sheet, que_number, ans_letter, col_starts, x_dist, y_dist, size_bubble)
    
for que_number, ans_letter in ans_2.items():
    correct_bubble(omr_sheet, que_number, ans_letter, col_starts, x_dist, y_dist, size_bubble)


omr = 'C:\\Users\\omkar\\OneDrive\\Desktop\\CV\\Ass1\\omr_correct_ans_3.png'
omr_sheet.save(omr, "PNG")
plt.imshow(omr_sheet)
plt.show()