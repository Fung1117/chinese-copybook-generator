import os
import requests
import numpy as np
import pinyin as py
from itertools import zip_longest
from pinyin.cedict import translate_word
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def get_chinese_word_png(chinese_word):
    unicode_hex = chinese_word.encode('unicode-escape').decode()[2:]
    image_path = f"assets/strokes/sequence/{unicode_hex}.png"

    # if os.path.exists(image_path):
    #     image = Image.open(image_path)
    #     width, height = image.size
    #     return image_path, height

    url = f"https://ckc.eduhk.hk/apps/strokes/sequence/200/{unicode_hex}.png"
    response = requests.get(url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        block_size = 200
        width, height = image.size
        num_blocks = width // block_size

        # Find the last non-white square block
        last_block = None
        for i in range(num_blocks-1, -1, -1):
            block = image.crop((i * block_size, 0, (i+1) * block_size - 8, block_size))
            pixels = np.array(block)
            if not np.all(pixels == 255):  # Check if the block is not entirely white
                last_block = block
                break

        # change the color
        image = image.convert("RGB")
        image_array = np.array(image)
        target_color = (0, 0, 0)
        target_channels = np.array(target_color)
        color_mask = np.all(image_array == target_channels, axis=2)
        image_array[color_mask] = [200, 200, 200]
        image = Image.fromarray(image_array)

        # merge the image
        new_image = Image.new("L", (width + block_size - 7, height))
        new_image.paste(last_block, (0, 0))
        new_image.paste(image, (block_size , 0))

        # save the image
        new_image.save(image_path)

        return image_path, width, height

def add_rice_grid(c, height):
    for index in range(1, 10):
        c.drawImage('assets/image/ricegrid.png', 50 * index, height, width=50, height=50)

# def add_vocabulary(c, vocabulary, pdf_height):
#     w, h = A4
#     max_dimension = 500
#     translation = translate_word(vocabulary)
    
#     for index, word in enumerate(vocabulary, start=1):

#         # pinyin = py.get(word, format='diacritical')
#         # c.setFillColorRGB(0, 0, 0)
#         # c.setFont("Cousine", 20)
#         # c.drawString(50 * index, h - pdf_height, pinyin)
        
#         c.drawImage('assets/image/ricegrid.png', 50 * index, h - pdf_height - 45 - 10, width=50, height=50)
#         add_rice_grid(c, 100)
#         c.setFillColorRGB(0.7845, 0.7845, 0.7845)
#         c.setFont("baseFont", 50)
#         c.drawString(50 * index, h - pdf_height - 45, word)


#     for index, word in enumerate(vocabulary, start=1):
#         image_path, width, height = get_chinese_word_png(word)
#         scaling_factor = min(max_dimension / width, max_dimension / height)
#         c.drawImage(image_path, 50, h - pdf_height - 45 * index - 60, width=int(width * scaling_factor), height=int(height * scaling_factor))

#     return pdf_height

def page_one(c, vocabularies):
    w, h = A4
    c.setFillColorRGB(0.7845, 0.7845, 0.7845)
    c.setFont("baseFont", 40)
    
    height = 50
    for index, (vocabulary1, vocabulary2) in enumerate(zip_longest(vocabularies[::2], vocabularies[1::2]), 1):
        c.rect(20, h - height - 100 * index, 177, 80)
        c.rect(20 + 177, h - height - 100 * index, 100, 80)
        c.rect(20 + 277, h - height - 100 * index, 177, 80)
        c.rect(20 + 277 + 177, h - height - 100 * index, 100, 80)
        w_height = height - 30 + 100 * index 
        x_start = 25
        for x, word in enumerate(vocabulary1):
            c.drawImage('assets/image/ricegrid.png', x_start + 40 * x , h - w_height - 10, width=40, height=40)
            c.drawString(x_start + 40 * x, h - w_height, word)
        x_start += 277
        if vocabulary2 is not None:
            for x, word in enumerate(vocabulary2):
                c.drawImage('assets/image/ricegrid.png', x_start + 40 * x , h - w_height - 10, width=40, height=40)
                c.drawString(x_start + 40 * x, h - w_height, word)
                    
def page_two(c, words):
    w, h = A4
    # c.showPage()
    p_height = 0 
    max_dimension = 500
    for index, word in enumerate(words):
        image_path, width, height = get_chinese_word_png(word)
        scaling_factor = max_dimension / width
        c.drawImage(image_path, 50, h - 50 - int(height * scaling_factor) - 10 * index, width=int(width * scaling_factor), height=int(height * scaling_factor))
        p_height = int(height * scaling_factor)


# 補
def generate_worksheet_pdf(vocabularies=['你好'], words='寶'):
    pdf_buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('baseFont', 'assets/font/DFPKaiShuW3-B5.ttf'))
    pdfmetrics.registerFont(TTFont('Cousine', 'assets/font/Cousine.ttf'))
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    page_one(c, vocabularies)
    page_two(c, words)
    c.save()
    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf_data

def test():
    get_chinese_word_png('你')
    pass

test()
