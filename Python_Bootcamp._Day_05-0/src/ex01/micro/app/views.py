import json

from flask import render_template, request
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import mimetypes
from app import app

UPLOAD_FOLDER = 'static/'
path = os.getcwd() + '/' + UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'wav'}
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
path = os.getcwd() + '/' + UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET"])
@app.route('/index')
def index():
    list_of_files = []
    for filename in os.listdir(path):
        list_of_files.append(filename)
    context = {'items': list_of_files}
    return render_template('index.html', **context)


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            return render_template("success.html", name=f.filename)
        else:
            return render_template("err.html")


@app.route("/list", methods=["GET"])
def get_list():
    list_of_files = []
    for filename in os.listdir(path):
        list_of_files.append(filename)
    response = app.response_class(
        response=json.dumps(list_of_files),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/upload', methods=['POST'])
def client_upload():
    if request.method == 'POST':
        f = request.files['file']
        mime_type, _ = mimetypes.guess_type(f.filename)
        if f and mime_type in ('audio/mpeg', 'audio/ogg', 'audio/x-wav'):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            response = app.response_class(
                response="OK",
                status=200,
                mimetype='text/plain'
            )
            return response
        else:
            response = app.response_class(
                response="Upload error",
                status=500,
                mimetype='text/plain'
            )
            return response
