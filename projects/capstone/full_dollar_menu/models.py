import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "capstone"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app, data_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = data_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    """Database object for a menu item."""
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # the required datatype is [{'ingredient_name': string, 'ingredient_amount': string}]
    category = Column(Integer)
    ingredients = Column(String(180), nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, name, ingredients, price, category):
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.category = category

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def _get_short_formatted_ingredients(self):
        ingredients = [{'ingredient': ingredient['ingredient_name']} for ingredient in json.loads(self.ingredients)]
        return ingredients

    def _get_long_formatted_ingredients(self):
        ingredients = [{'ingredient': ingredient['ingredient_name'], 'amount': ingredient['ingredient_amount']}
                       for ingredient in json.loads(self.ingredients)]
        return ingredients

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'ingredients': self._get_short_formatted_ingredients(),
            'category': self.category
        }

    def long_format(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'ingredients': self._get_long_formatted_ingredients(),
            'category': self.category
        }


class Category(db.Model):
    __tablename__ = 'categories'
    """Database object for a category item."""
    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
