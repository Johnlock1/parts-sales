import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


if __name__ == '__main__':
    app.run()
