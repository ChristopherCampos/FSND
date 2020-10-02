import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "menu.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


db.create_all()


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    """Database object for a menu item."""
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    recipe = Column(String(180), nullable=False)

    def __init__(self, name, recipe, category):
        self.name = name
        self.recipe = recipe
        self.category = category

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'recipe': json.loads(self.recipe),
            'category': self.category
        }


class Category(db.Model):
    __tablename__ = 'catagories'
    """Database object for a category item."""
    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }