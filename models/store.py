from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') #self isn't a list of items, it's a query builder

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name, 'items': [item.json() for item in self.items.all()]} #tradeoff of speed of creation of store vs speed of lookup of items

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #SELECT * from TABLE_NAME WHERE name=name, LIMIT=1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

