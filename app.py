from flask import Flask, render_template, make_response, request
from worksheet import generate_worksheet_pdf

app = Flask(__name__)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    if request.method == 'POST':
        user_input = request.json.get('text', [])
        if user_input:
            pdf_content = generate_worksheet_pdf(user_input)
        else:
            pdf_content = generate_worksheet_pdf()
        response = make_response(pdf_content)
        response.headers["Content-Type"] = "application/pdf"
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response
    else:
        pdf_content = generate_worksheet_pdf()
        response = make_response(pdf_content)
        response.headers["Content-Type"] = "application/pdf"
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response 

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)