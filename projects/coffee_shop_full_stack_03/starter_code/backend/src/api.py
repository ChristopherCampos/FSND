import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth, check_permissions, verify_decode_jwt, get_token_auth_header

app = Flask(__name__)
setup_db(app)
CORS(app)
####

def auth(permission):
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    check_permissions(permission, payload)

####
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@requires_auth
@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        return jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@requires_auth(permission='get:drinks-detail')
@app.route('/drinks-detail')
def get_drink_details():
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        return jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@requires_auth(permission='post:drinks')
@app.route('/drinks', methods=['POST'])
def add_drink():
    body = request.get_json()
    if body is None:
        abort(422)
    if body.get('title') and body.get('recipe'):
        try:
            new_title = body.get('title')
            new_recipe = body.get('recipe')
            new_drink = Drink(title=new_title, recipe=new_recipe)
            new_drink.insert()
            drinks = Drink.query.order_by(Drink.id).all()
            return jsonify({"success": True,
                            "drinks": [drink.long() for drink in drinks]
                            })
        except:
            abort(422)
    else:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@requires_auth(permission='patch:drinks')
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def edit_drink(drink_id):
    body = request.get_json()
    if body is None:
        abort(422)
    if body.get('title') and body.get('recipe'):
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            drink.title = body.get('title')
            drink.recipe = body.get('recipe')
            drink.update()
            drinks = Drink.query.order_by(Drink.id).all()
            return jsonify({'success': True,
                            'drinks': [drink.long() for drink in drinks]
                            })
        except:
            abort(422)
    else:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@requires_auth(permission='delete:drinks')
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def not_found(error):
    return jsonify({
            'success': False,
            'error': 401,
            'message': 'permission denied'
        }), 401

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def not_found(error):
    return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code
