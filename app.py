from flask import Flask, render_template, make_response, request, send_file
from worksheet import generate_worksheet_pdf

app = Flask(__name__)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    if request.method == 'POST':
        vocabularies = request.json.get('vocabularies', [])
        words = request.json.get('words', '')
        pdf_content = generate_worksheet_pdf(vocabularies, words)
        response = make_response(pdf_content)
        response.headers["Content-Type"] = "application/pdf"
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response
    else:
        pdf_content = generate_worksheet_pdf(['你好'], '你好')
        response = make_response(pdf_content)
        response.headers["Content-Type"] = "application/pdf"
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response 

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)