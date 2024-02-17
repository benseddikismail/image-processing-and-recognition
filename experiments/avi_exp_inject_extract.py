import os

import qrcode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PIL import Image
from pyzbar.pyzbar import decode

LINE_LENGTH = 4 


def pad_line(data):
    return data.ljust(LINE_LENGTH, b" ")


def unpad_line(data):
    return data.rstrip(b" ")


def encrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as file:
        plaintext = file.read()

    backend = default_backend()
    iv = os.urandom(16) 
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    padded_plaintext = b"\n".join(map(pad_line, plaintext.split(b"\n")))
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    print("Encrypted text from GroundTruth")
    print(ciphertext)

    with open(output_file, "wb") as file:
        file.write(iv + ciphertext)


def create_qr_code(data, output_filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_filename)


# b'k\xa5\x8f\xf9\x0fO\xcd\xe4^,\x90kI\xff\xaf(`+\xc5\xa4\x0c\x05\xab\x83u\xf9\x1b,\xb3\x91Xv'
# b'\xacT\x1e\xe3\xcf&\xbbo5\x83\xbcU]\x19>\x10;\xa5\x9e\xeb\x985\xa6\xbd\xf0\xfb\xa6\x85\x87&\xb1\x06'


def decrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as file:
        data = file.read()

    iv = data[:16]  
    ciphertext = data[16:]

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadded_plaintext = b"\n".join(map(unpad_line, plaintext.split(b"\n")))

    with open(output_file, "wb") as file:
        file.write(unpadded_plaintext)


def read_qr_code(image_path, output_file_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)

    if decoded_objects:
        with open(output_file_path, "wb") as file:
            file.write(decoded_objects[0].data)
        return decoded_objects[0].data


ground_truth_file = "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/test-images/a-27_groundtruth.txt"

input_file = "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/test-images/a-27_groundtruth.txt"
output_file = "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/encrypted_ciphertext.txt"
key = os.urandom(32)  
print("key =" + str(key))
encrypt_file(input_file, output_file, key)
print("Encryption complete.")

decrypted_output_file = "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/decrypted.txt"
decrypt_file(output_file, decrypted_output_file, key)
print("Decryption complete.")

with open(
    "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/encrypted_ciphertext.txt",
    "rb",
) as file:
    ciphertext = file.read()

ciphertext_str = ciphertext.decode("latin-1")

create_qr_code(
    ciphertext_str,
    "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/encrypted_qr.jpg",
)
print("QR Code generated.")

qr_code_image_path = "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/encrypted_qr.jpg"

output_file = "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/encrypted_text_from_qr.txt"
encrypted_text_from_qr = read_qr_code(qr_code_image_path, output_file)
print("Encrypted text from the QR code")
print(encrypted_text_from_qr)


decrypted_output_file = "/Users/avishmita/IU_Reading_Material/IU/Computer Vision/Assignments/Assignment_1/decrypted_final.txt"
decrypt_file(output_file, decrypted_output_file, key)
print("Decryption complete.")
