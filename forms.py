from wtforms import Form, DateField, IntegerField, FloatField, StringField


class SalesSearchForm(Form):
    search = StringField('Search', render_kw={'placeholder': 'Search date'})


class NewSaleForm(Form):
    date = DateField('Date')
    parts = StringField('Parts')
    car_model = StringField('Car Model')
    item_count = IntegerField('Item Count')
    value = FloatField('Value')
