import os
from flask import Flask, flash, Markup, redirect, render_template, request, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.abspath(os.path.dirname('uploads')) + '/uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

from import_file import *
from models import *
from tables import *
from forms import NewSaleForm, SalesSearchForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    results = Sales.query.order_by(Sales.date).all()
    total = sum([sale.value for sale in results])

    table = Results(results)

    search = SalesSearchForm(request.form)
    if request.method == 'POST':
        return search_sales(search)
    # table.border = True
    return render_template('sales.html', table=table, form=search, sum=total)


@app.route('/search_sales')
def search_sales(search):
    results = []
    search_string = search.data['search']

    if search_string == '':
        return redirect('/sales')

    # display results
    try:
        results = Sales.query.filter_by(date=search_string).all()
        total = sum([sale.value for sale in results])

        table = Results(results)
        form = SalesSearchForm(request.form)
        return render_template('sales.html', table=table, form=form, sum=total)

    # can't perform select query
    except Exception as e:
        db.session.rollback()
        flash('No results found!')
        return redirect('/sales')


@app.route('/chart')
def chart():
    dates = db.session.query(Sales.date).distinct(Sales.date).order_by(Sales.date).all()
    labels = [date[0].strftime('%Y/%m/%d') for date in dates]
    # print(labels)
    vals = db.session.query(func.sum(Sales.value)).group_by(Sales.date).order_by(Sales.date).all()
    values = [float(v[0]) for v in vals]
    # print(values)

    avgs = db.session.query(func.avg(Sales.value)).group_by(Sales.date).order_by(Sales.date).all()
    averages = [float(a[0]) for a in avgs]

    return render_template('chart.html', labels=labels, values1=values, values2=averages)
    # return redirect(url_for('index'))

# @app.route('/new', methods=['GET', 'POST'])
# def new():
#     form = NewSaleForm(request.form)
#     return render_template('new.html', form=form)


@app.route('/import', methods=['GET', 'POST'])
def importing():
    if request.method == 'POST':
        date = request.form.get('date')
        value = request.form.get('value')

        # date & value columns of db have a NOT NULL restriction
        if date == "" or value == "":
            flash("Date or value inputs where empty")
            return redirect(request.url)

        parts = request.form.get('parts') or None
        car_model = request.form['car_model'] or None
        item_count = request.form.get('item_count') or None

        # save to db
        sale = Sales(date=date, parts=parts, car_model=car_model,
                     item_count=item_count, value=value)
        db.session.add(sale)
        db.session.commit()

        flash('Success! Sale was saved.')

    return render_template('import.html')


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    templates = os.path.abspath(os.path.dirname('download')) + '/download'
    print(templates)
    return send_from_directory(directory=templates, filename=filename, as_attachment=True)


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

        # upload and save & import data from it.
        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            import_file(file)
            flash('Success! File was uploaded.')

    return redirect(url_for('importing'))


if __name__ == '__main__':
    app.run()
