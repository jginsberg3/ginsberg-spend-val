from app import app
from app.static.scripts.check_file import check_file
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os 


@app.route("/")
def index():
    return "Hello Horizon Next!"


def allowed_file(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_DOC_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload-multi-files", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        if request.files:
            print("FILES: \n")
            files_dict = request.files.to_dict(flat=False)
            print(files_dict)
            accepted_list = []
            failed_list = []
            for file in files_dict['uploadfiles']:
                if file.filename == '':
                    print('No file name')
                    pass
                elif allowed_file(file.filename): 
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config["DOC_UPLOADS"], filename)
                    file.save(file_path)
                    print(file)
                    print('Loaded file: {}'.format(file_path))
                    _file_check = check_file(file_path)
                    if _file_check[0] == True:
                        accepted_list.append(filename)
                    else:
                        failed_list.append((filename, _file_check[1]))
                        print('ERROR: file {} did not pass validator!'.format(file.filename))
                else:
                    print('File extension not allowed!  Did not upload file: {}'.format(file.filename))
                    failed_list.append((file.filename, 'File extension not allowed.'))
            print('ACCEPTED LIST:')
            print(accepted_list)
            print('FAILED LIST:')
            print(failed_list)
            print('\n')
            print('URL: ' + str(request.url))
            return render_template("public/upload_files.html", accepted_list=accepted_list, failed_list=failed_list)
    return render_template("public/upload_files.html")
