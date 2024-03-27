from flask import Flask, render_template, request, redirect, url_for
from docx import Document
import PyPDF2;

app = Flask(__name__)

ls = {} #dictionary to store all filename and data

@app.route('/')
def upload_form():
  return render_template('upload.html',text=ls)

@app.route('/output/<filename>')
def output_page(filename):
  text = ls[filename]
  return render_template('output.html',text=text,file=filename.rsplit('.',1)[0].capitalize())

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_extension = filename.rsplit('.',1)[1].lower()
    
    """ #text
    if file_extension == 'txt':
      text = file.read().decode('utf-8')   """

    #word
    if file_extension == 'docx':
      text = ''
      document = Document(file)
      for paragraph in document.paragraphs:
        text += paragraph.text+'\n'
    
    #pdf
    elif file_extension == 'pdf':
      text = ''
      reader = PyPDF2.PdfReader(file)
      for page in reader.pages:
        text += page.extract_text()

    else:
      return render_template('upload.html',message='*Only .txt and .docx file supported!')

    ls.update({filename:text})
    
    return redirect(url_for('upload_form'))

#error
@app.errorhandler(500)
def error(e):
  return render_template('upload.html',message=e)

if __name__ == "__main__":
    app.run(debug=True)