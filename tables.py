from flask_table import Table, Col, LinkCol


class Results(Table):

    id = Col('Id', show=False)
    date = Col('Date')
    parts = Col('Parts')
    car_model = Col('Car Model')
    item_count = Col('Item Count')
    value = Col('Value')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
