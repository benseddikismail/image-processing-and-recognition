import barcode
from barcode.writer import ImageWriter

def barcode_create(url, output_file):
    CODE = barcode.get_barcode_class('code128')
    barcode_instance = CODE(url, writer=ImageWriter())
    barcode_instance.save(output_file)

url = "https://imgur.com/a/hCtOxAQ"
output_file = "barcode"
barcode_create(url, output_file)
