import sys

from PIL import Image
from pyzbar.pyzbar import decode


def read_qr_code(image, output_file_path):

    # Decode the QR code
    decoded_objects = decode(image)

    if decoded_objects:
        with open(output_file_path, "wb") as file:
            file.write(decoded_objects[0].data)
        return decoded_objects[0].data


def extract_qr(injected_form):
    form_width, form_height = injected_form.size

    x_coordinate = form_width - 180
    y_coordinate = 0

    qr_region = injected_form.crop((x_coordinate, y_coordinate, form_width, 180))
    qr_region.show()

    return qr_region


if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception(
            "error: please give an input image name as a parameter, like this: \n"
            "python3 ./extract.py injected.jpg output.txt"
        )

    injected_form = Image.open(sys.argv[1])
    correct_answer_text_file = sys.argv[2]

    extracted_qr_img = extract_qr(injected_form)

    read_qr_code(extracted_qr_img, correct_answer_text_file)
