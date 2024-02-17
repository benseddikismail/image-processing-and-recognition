from PIL import Image

img_a = Image.open("a-27.jpg").convert("RGB")
# img_a = Image.open("a-3.jpg").convert("RGB")
img_b = Image.open("omr_correct_ans_3.png").convert("RGB")


if img_a.size != img_b.size:
    raise ValueError("Images are not the same size")

def overlay_images(img1, img2):
    res_img = Image.new("RGB", img1.size)
    pix1 = img1.load()
    pix2 = img2.load()
    res_pix = res_img.load()

    for y in range(img1.size[1]):
        for x in range(img1.size[0]):
            if pix1[x, y] == pix2[x, y]:
                res_pix[x, y] = (0, 255, 0) if pix1[x, y] == (0, 0, 0) else pix1[x, y]
            else:
                res_pix[x, y] = (255, 0, 0) if pix1[x, y] == (0, 0, 0) else pix1[x, y]
    return res_img

res = overlay_images(img_a, img_b)

res_path = "C:\\Users\\omkar\\OneDrive\\Desktop\\CV\\Ass1\\overlay_result_27.png"
res.save(res_path)
res_path
