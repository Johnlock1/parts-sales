from app import db
from sqlalchemy import Sequence


class Sales(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    parts = db.Column(db.Text)
    car_model = db.Column(db.Text)
<<<<<<< HEAD
    item_count = db.Column(db.Integer, default=1)
    value = db.Column(db.Numeric(6, 2), nullable=False)
||||||| merged common ancestors
    item_count = db.Column(db.Integer, default=1)
    value = db.Column(db.Numeric(4, 2), nullable=False)
=======
    item_count = db.Column(db.Integer)
    value = db.Column(db.Numeric(6, 2), nullable=False)
>>>>>>> development

    def __init__(self, date, parts, car_model, item_count, value):
        self.date = date
        self.parts = parts
        self.car_model = car_model
        self.item_count = item_count
        self.value = value

    def __repr__(self):
        return f'{self.id}, {self.date}'
