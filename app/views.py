from app import app
from app.static.scripts.check_file import check_file
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os 
import logging

logging.basicConfig(level=logging.INFO)


@app.route("/")
def index():
    return "Hello Horizon Next!"


@app.route("/validate-files", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        try:
            files_dict = request.files.to_dict(flat=False)
            
            accepted_list, failed_list = validate_file_list(files_dict)

            logging.info('ACCEPTED LIST:')
            logging.info(accepted_list)
            logging.info('FAILED LIST:')
            logging.info(failed_list)

            return render_template("public/upload_files.html",
                accepted_list=accepted_list, failed_list=failed_list)

        except Exception as e:
            logging.warning('ERROR: files not found in request.')
            logging.warning(e)
            return render_template("public/upload_files.html")

    if request.method == "GET":
        return render_template("public/upload_files.html")


def validate_file_list(files_dict):
    accepted_list = []
    failed_list = []

    for file in files_dict['uploadfiles']:
        if file.filename == '':
            logging.warning('No file name')
            pass
        elif not allowed_file(file.filename): 
            filename = secure_filename(file.filename)
            logging.warning('File extension not allowed!  Did not upload file: {}'.format(
                file.filename))
            failed_list.append((file.filename, 'File extension not allowed.'))
        else:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["DOC_UPLOADS"], filename)
            file.save(file_path)
            logging.info('Loaded file: {}'.format(file_path))
            _file_check = check_file(file_path)
            if _file_check[0] == False:
                failed_list.append((filename, _file_check[1]))
                logging.warning('ERROR: file {} did not pass validator!'.format(
                    file.filename))
            else:
                accepted_list.append(filename)

    return (accepted_list, failed_list)

def allowed_file(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if not ext.upper() in app.config["ALLOWED_DOC_EXTENSIONS"]:
        return False
    else:
        return True
