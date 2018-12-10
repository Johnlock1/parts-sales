import os
<<<<<<< HEAD
from decimal import Decimal
from flask import Flask, redirect, render_template, request, url_for
||||||| merged common ancestors
from flask import Flask, redirect, render_template, request, url_for
=======
from flask import Flask, flash, redirect, render_template, request, url_for
>>>>>>> development
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath(os.path.dirname('uploads')) + '/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'xls', 'xlsx'])

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

from import_file import *
from models import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sales')
def sales():
    sales = Sales.query.order_by(Sales.date).all()

    return render_template('sales.html', sales=sales)


@app.route('/import', methods=['GET', 'POST'])
def importing():
    if request.method == 'POST':
        date = request.form.get('date')
        value = request.form.get('value')

        # date & value columns of db have a NOT NULL restriction
        if date == "" or value == "":
<<<<<<< HEAD
            print("Error! Empty date or value")
        else:
            print(f"{date}, {parts}, {car_model}, {item_count}, {value}")
            print(type(value))
            try:
                sale = Sales(date=date, parts=parts, car_model=car_model,
                             item_count=item_count, value=value)
                db.session.add(sale)
                db.session.commit()
            except:
                db.session.rollback()
                raise
        return redirect(url_for(('importing')))
    else:
        return render_template('import.html')
||||||| merged common ancestors
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
=======
            flash("Date or value inputs where empty")
            return redirect(request.url)

        parts = request.form.get('parts', None)
        car_model = request.form.get('car_model', None)
        item_count = request.form.get('item_count', None)

        # convert empty string to None
        if parts == "":
            parts = None
        if car_model == "":
            car_model = None
        if item_count == "":
            item_count = None

        # save to db
        sale = Sales(date=date, parts=parts, car_model=car_model,
                     item_count=item_count, value=value)
        db.session.add(sale)
        db.session.commit()

        flash('Success! Sale was saved.')

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
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            import_file(file)
            flash('Success! File was uploaded.')

    return redirect(url_for('importing'))
>>>>>>> development


if __name__ == '__main__':

    app.run()
