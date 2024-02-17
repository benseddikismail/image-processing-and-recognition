from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import requests
from io import BytesIO

def get_url(embed_code):

    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    with webdriver.Chrome(opts=opts) as driver:
        driver.get("data:text/html;charset=utf-8," + embed_code)
        try:
            img_ele = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.imgur-embed-pub"))
            )
            return img_ele.get_attribute('src')
        except:
            print("Image not found or took too long to load.")

def disp_img_from_url(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        img = Image.open(BytesIO(resp.content))
        img.show()
    else:
        print(f"Failed to fetch img from URL: {url}")

embed_code = '''<blockquote class="imgur-embed-pub" lang="en" data-id="a/hCtOxAQ" data-context="false" ><a href="//imgur.com/a/hCtOxAQ"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>'''
img_url = get_url(embed_code)
if img_url:
    print(f"Image URL: {img_url}")
    disp_img_from_url(img_url)
    