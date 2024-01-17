import requests
import pinyin as py
from pinyin.cedict import translate_word
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def get_chinese_word_png(chinese_word):
    unicode_hex = chinese_word.encode('unicode-escape').decode()[2:]
    url = f"https://ckc.eduhk.hk/apps/strokes/sequence/200/{unicode_hex}.png"

    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        return url, width, height

def add_vocabulary(c, vocabulary):
    w, h = A4
    max_dimension = 500
    translation = translate_word(vocabulary)

    for word in vocabulary:

        c.drawImage('asset/image/ricegrid.png', 50, h - 60 - 10, width=50, height=50)
        c.setFillColorRGB(0.7845, 0.7845, 0.7845)
        c.setFont("baseFont", 50)
        c.drawString(50, h-60, word)

        pinyin = py.get(word, format='diacritical')
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Cousine", 20)
        c.drawString(50, h - 60 + 45, pinyin)
        
        url, width, height = get_chinese_word_png(word)
        scaling_factor = min(max_dimension / width, max_dimension / height)
        c.drawImage(url, 50, h - 200, width=int(width * scaling_factor), height=int(height * scaling_factor))
    
def generate_worksheet_pdf():
    pdf_buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('baseFont', 'asset/font/DFPKaiShuW3-B5.ttf'))
    pdfmetrics.registerFont(TTFont('Cousine', 'asset/font/Cousine.ttf'))
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    add_vocabulary(c, '聰')

    c.save()
    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf_data