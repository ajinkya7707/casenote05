from flask import Flask, render_template, session, request, redirect, url_for
from script import process_csv_with_columns
from script import process_csv_with
from script import process_columns
from script import process_csv_with_chart
from script import patientinsights1
from script import patientinsights2
from script import patientinsights3
from script import additionalques
from PIL import Image
import base64
import io
import secrets

app = Flask(__name__, static_url_path='/static')
text = ""  # Initialize text as a global variable
app.secret_key = secrets.token_hex(16)  # Generate a secure random key

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Save the uploaded file
    # (Add your file saving logic here)

    # Return a success message
    return 'File uploaded successfully!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/About')
def about():
    return render_template('about.html')

@app.route('/Upload')
def upload():
    return render_template('upload.html')

@app.route('/CaseNote Insight')
def casenote():
    return render_template('casenote.html')

@app.route('/Another Route')
def casenotee():
    return render_template('casenote.html')

@app.route('/Patient Insight')
def patient():
    return render_template('patient.html')

@app.route('/process', methods=['GET','POST'])
def process():
    if request.method == 'POST':
        file = request.files['file']
        #print(f"Received file: {file.filename}")
        file.save(file.filename)
        # Store user input in the session
        session['file_input'] = file.filename
        global output1
        output1 = process_csv_with_columns(file.filename)
        global output2
        global img_data1
        output2 = process_csv_with(file.filename)
        im = Image.open(output2)
        data = io.BytesIO()
        im.save(data, "PNG")
        img_data1 = base64.b64encode(data.getvalue())

        global output3
        global img_data2
        output3 = process_columns(file.filename)
        im = Image.open(output3)
        data = io.BytesIO()
        im.save(data, "PNG")
        img_data2 = base64.b64encode(data.getvalue())

        global output4
        global img_data3
        output4 = process_csv_with_chart(file.filename)
        im = Image.open(output4)
        data = io.BytesIO()
        im.save(data, "PNG")
        img_data3 = base64.b64encode(data.getvalue())

    return render_template('casenote.html', answer1=output1, answer2=img_data1.decode('utf-8'), answer3=img_data2.decode('utf-8'), answer4 = img_data3.decode('utf-8'))


@app.route('/add_data', methods=['GET','POST'])
def add_data():
    global text
    text = session.get('file_input', '')
    if request.method == 'POST':
        # Store new user input in the session
        session['case_note'] = request.form.get('case_note')
        session['add_ques'] = request.form.get('add_ques')
        text = request.form.get('case_note')
        #ques = request.form.get('add_ques')
        global output11
        output11 = patientinsights1(text)

        global output12
        output12 = patientinsights2(text)

        global output13
        output13 = patientinsights3(text)

        #global output14
        #output14 = additionalques(text, ques)


    return render_template('patient.html', answer11=output11, answer12=output12, answer13=output13)

@app.route('/mp_data', methods=['GET','POST'])
def mp_data():
    global text
    text = session.get('file_input', '')
    add_ques = session.get('add_ques', '')
    if request.method == 'POST':
        ques = request.form.get('add_ques')
        global output
        output = additionalques(text, ques)
    return render_template('patient.html', answer = output)


if __name__ == '__main__':
    app.run(debug=True)

