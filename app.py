import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath(os.path.dirname('uploads')) + '/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'xls', 'xlsx'])

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

from models import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sales')
def sales():
    sales = Sales.query.all()
    return render_template('sales.html', sales=sales)


@app.route('/import', methods=['GET', 'POST'])
def importing():
    if request.method == 'POST':
        date = request.form.get('date')
        parts = request.form.get('parts')
        car_model = request.form.get('car_model')
        item_count = request.form.get('item_count')
        value = request.form.get('value')
        if date == "" or value == "":
            print("Error! Empty date or value")
        else:
            print(f"{date}, {parts}, {car_model}, {item_count}, {value}")
            sale = Sales(date=date, parts=parts, car_model=car_model,
                         item_count=item_count, value=value)
            db.session.add(sale)
            db.session.commit()
        return redirect(url_for(('importing')))
    else:
        return render_template('import.html')

# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file parts
        if 'file' not in request.files:
            flash('No file was selected')
            return redirect(request.url)
        file = request.files['file']
        # if the user does not select file, browser also
        # submit and empty part without filename
        if file.name == '':
            flash('No selected file')
            return redirect(request.url)
        # if users submit file with ext. not in ALLOWED_EXTENSIONS
        if not allowed_file(file.filename):
            flash('File extension isn\'t allowed')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Success! File was uploaded.')

    return redirect(url_for('importing'))


if __name__ == '__main__':
    print(UPLOAD_FOLDER)
    app.run()
