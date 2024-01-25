from flask import Flask, render_template, make_response, request, send_file
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

@app.route('/exam_files')
def exam_files():
    years = [2019, 2020, 2021, 2022, 2023]  # List of years
    return render_template('exam_files.html', years=years)

@app.route('/download_pdf/<int:year>')
def get_pdf_file(year):
    # Logic to fetch and return the PDF file for the given year
    # Replace the placeholder code with your actual implementation
    pdf_file = f"exam_{year}.pdf"
    return send_file(pdf_file, as_attachment=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)