from flask import Flask, abort, jsonify
from .database.models import setup_db, MenuItem, Category
from .auth.auth import requires_auth
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/menu', methods=['GET'])
    def get_menu():
        """Returns all of the menu items in the database"""
        try:
            items = MenuItem.query.order_by(MenuItem.id).all()
            return jsonify({
                "success": True,
                "drinks": [menu_item.format() for menu_item in items]
            })
        except Exception:
            abort(404) # (Change)Authentication error

    @app.route('/menu/categories', methods=['GET'])
    def get_menu_categories():
        """Returns all of the menu item categories in the database"""
        try:
            categories = Category.query.order_by(Category.id).all()
            return jsonify({
                "success": True,
                "categories": [category.format() for category in categories]
            })
        except Exception:
            abort(404)  # (Change)Authentication error

    @app.route('/menu', methods=['POST'])
    @app.route('/menu', methods=['PATCH'])
    @app.route('/menu/<int:id>/delete', methods=['DELETE'])



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

    #@app.errorhandler(AuthError)
    #def not_found(error):
    #    return jsonify({
    #        'success': False,
    #        'error': error.status_code,
    #        'message': error.error
    #    }), error.status_code

    return app


APP = create_app()






if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
