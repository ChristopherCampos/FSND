from flask import Flask, abort, jsonify, request
from models import setup_db, MenuItem, Category
from auth import requires_auth, AuthError
from flask_cors import CORS
import json


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    def format_ingredients(ingredients_dictionary):
        formatted_recipe = json.dumps(ingredients_dictionary)
        formatted_recipe = '[' + formatted_recipe + ']'
        return formatted_recipe

    @app.route('/menu', methods=['GET'])
    def get_menu():
        """Returns all of the menu items in the database"""
        try:
            items = MenuItem.query.order_by(MenuItem.id).all()
            return jsonify({
                "success": True,
                "menu_items": [menu_item.format() for menu_item in items]
            })
        except Exception:
            abort(422) # (Change)Authentication error

    @app.route('/menu/categories/<int:category_id>', methods=['GET'])
    @requires_auth(permission='get:menu_item')
    def get_menu_items_by_category(token, category_id):
        """Returns all of the menu item categories in the database"""
        try:
            menu_items = MenuItem.query.filter(MenuItem.category == category_id).all()
            return jsonify({
                "success": True,
                "category_id": category_id,
                "items": [menu_item.format() for menu_item in menu_items]
            })
        except Exception:
            abort(422)

    @app.route('/menu/categories', methods=['GET'])
    @requires_auth(permission='get:categories')
    def get_menu_categories(token):
        """Returns all of the menu item categories in the database"""
        try:
            categories = Category.query.order_by(Category.id).all()
            return jsonify({
                "success": True,
                "categories": [category.format() for category in categories]
            })
        except Exception:
            abort(422)  # (Change)Authentication error

    @app.route('/menu/categories', methods=['POST'])
    @requires_auth(permission='post:categories')
    def add_category(token):
        """Adds a new category to the menu."""
        body = request.get_json()
        if body is None:
            abort(422)
        try:
            new_type = body.get('type')
            new_category = Category(type=new_type)
            new_category.insert()
            categories = Category.query.order_by(Category.id).all()
            return jsonify({"success": True,
                            "categories": [category.format() for category in categories]
                            })
        except Exception:
            abort(422)

    @app.route('/menu', methods=['POST'])
    @requires_auth(permission='post:menu_item')
    def add_menu_item(token):
        """Adds a new menu item to the menu."""
        body = request.get_json()
        if body is None:
            abort(422)
        try:
            new_name = body.get('name')
            new_ingredients = body.get('ingredients')
            new_price = body.get('price')
            new_category = body.get('category')
            new_item = MenuItem(name=new_name, category=new_category, ingredients=new_ingredients, price=new_price)
            new_item.insert()
            menu_items = MenuItem.query.order_by(MenuItem.id).all()
            return jsonify({"success": True,
                            "menu_items": [menu_item.format() for menu_item in menu_items]
                            })
        except Exception:
            abort(422)

    @app.route('/menu/<int:item_id>', methods=['PATCH'])
    @requires_auth(permission='patch:menu_item')
    def edit_item(token, item_id):
        """Updates the given menu item with requested changes"""
        body = request.get_json()
        if body is None:
            abort(422)
        if body.get('name') or body.get('ingredients') or body.get('price') or body.get('category'):
            changed_item = MenuItem.query.filter(MenuItem.id == item_id).one_or_none()
            if changed_item is None:
                abort(422)
            try:
                if body.get('name'):
                    changed_item.name = body.get('name')
                if body.get('recipe'):
                    changed_item.ingredients = format_ingredients(body.get('ingredients'))
                if body.get('price'):
                    changed_item.price = body.get('price')
                if body.get('category'):
                    changed_item.category = body.get('category')
                changed_item.update()
                menu_items = MenuItem.query.order_by(MenuItem.id).all()
                return jsonify({"success": True,
                                "menu_items": [menu_item.format() for menu_item in menu_items]
                                })
            except Exception:
                abort(422)

    @app.route('/menu/<int:item_id>', methods=['DELETE'])
    @requires_auth(permission='delete:menu_item')
    def delete_item(token, item_id):
        try:
            menu_item = MenuItem.query.filter(MenuItem.id == item_id).one_or_none()
            if menu_item is None:
                abort(404)

            menu_item.delete()
            return jsonify({
                'success': True,
                'menu_item_id': item_id

            })
        except Exception:
            abort(422)

    @app.route('/menu/categories/<int:category_id>', methods=['DELETE'])
    @requires_auth(permission='delete:categories')
    def delete_category(token, category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                abort(404)

            category.delete()
            return jsonify({
                'success': True,
                'category_id': category_id

            })
        except Exception:
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'permission denied'
        }), 401

    @app.errorhandler(AuthError)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
