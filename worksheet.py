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

def get_chinese_word_png(unicode_hex):
    # unicode_hex = chinese_word.encode('unicode-escape').decode()[2:]
    image_path = f"assets/strokes/sequence/{unicode_hex}.png"

    if os.path.exists(image_path):
        image = Image.open(image_path)
        width, height = image.size
        return image_path, width, height

    url = f"https://ckc.eduhk.hk/apps/strokes/sequence/200/{unicode_hex}.png"
    response = requests.get(url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        # change the color
        image = image.convert("RGB")
        image_array = np.array(image)
        target_color = (0, 0, 0)
        target_channels = np.array(target_color)
        color_mask = np.all(image_array == target_channels, axis=2)
        image_array[color_mask] = [200, 200, 200]
        image = Image.fromarray(image_array)
        width, height = image.size

        # save the image
        image.save(image_path)

        return image_path, width, height

def get_chinese_image(chinese_word):
    unicode_hex = chinese_word.encode('unicode-escape').decode()[2:]
    image_path = f"assets/strokes/sequence/{unicode_hex}.png"
    absolute_path = os.path.abspath(image_path)
    if os.path.exists(absolute_path):
        image = Image.open(absolute_path)
        width, height = image.size
        return absolute_path, width, height


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
    c.showPage()
    p_heigth = 0
    c.setFont("baseFont", 38)
    max_dimension = 460
    for index, word in enumerate(words):
        image_path, width, height = get_chinese_image(word)
        scaling_factor = max_dimension / width
        c.drawImage(image_path, 90, h - 50 - height * scaling_factor - 10 * index - p_heigth, width=width * scaling_factor, height=height * scaling_factor)
        
        if (height * scaling_factor > 70):
            c.drawImage('assets/image/ricegrid.png', 50, h - 50 - height * scaling_factor - 10 * index - p_heigth + 37, width=38, height=38)
            c.drawString( 50, h - 50 - height * scaling_factor - 10 * index - p_heigth + 7 + 37, word)
        else:
            c.drawImage('assets/image/ricegrid.png', 50, h - 50 - height * scaling_factor - 10 * index - p_heigth, width=38, height=38)
            c.drawString( 50, h - 50 - height * scaling_factor - 10 * index - p_heigth + 7, word)
            
        p_heigth += height * scaling_factor


def generate_worksheet_pdf(vocabularies, words):
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

def download_png():
    start_range = 0x5787
    end_range = 0x5E0A
    # end_range = 0x9FFF

    for code_point in range(start_range, end_range + 1):
        unicode_hex = hex(code_point)[2:].lower().zfill(4)
        get_chinese_word_png(unicode_hex)

download_png()