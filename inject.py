import sys

import qrcode
from PIL import Image


def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


if __name__ == "__main__":

    if len(sys.argv) != 4:
        raise Exception(
            "error: please give an input image name as a parameter, like this: \n"
            "python3 ./inject.py form.jpg answers.txt injected.jpg"
        )

    with open(
        sys.argv[2],
        "rb",
    ) as file:
        text = file.read()

    form_img = Image.open(sys.argv[1])
    text_str = text.decode("latin-1")

    # Generate the QR code
    qr_img = create_qr_code(text_str)
    qr_img = qr_img.resize((180, 180))

    form_width, form_height = form_img.size

    qr_code_position = (form_width - qr_img.width, 0)
    form_img.paste(qr_img, qr_code_position)

    injected_file = sys.argv[3]
    form_img.save(injected_file)

    form_img.show()
