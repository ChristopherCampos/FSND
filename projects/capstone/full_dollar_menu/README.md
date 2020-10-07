# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/full_dollar_menu` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
dropdb capstone && createdb capstone
```

## Running the server

From within the `full_dollar_menu` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to run the flask application.

The link associated for my specific project is https://chris-campos.us.auth0.com/authorize?audience=fdm&response_type=token&client_id=3dAm6kZYfeaCxH6ehGUHR3V6MMrbXlj0&redirect_uri=https://full-dollar-menu.herokuapp.com/menu
## API Reference
Endpoints

GET '/menu'
- Request Arguments: None
- Returns: success and the menu items in the database 
- Example: `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X GET https://full-dollar-menu.herokuapp.com/menu'
`

-Output: `{'success': True, "menu_items": []}`

GET '/menu/categories'
- Request Arguments: None
- Example: `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X GET https://full-dollar-menu.herokuapp.com/menu/categories'
`

-Output: `{'success': True, ['name': type,...]}}`

GET '/menu/categories/(category_id)'
- Request Arguments: None
- Example: `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X GET https://full-dollar-menu.herokuapp.com/menu/categories/1'
`

-Output: `{'success': True, 'name': 'name', 'id': id}}`

POST '/menu'
- Adds a menu item to the API
- Request Arguments: name, ingredients, category, price
- Example:  `curl -i -H "Accept: application/json" -d '{"name": "spaghetti", "ingredients" : "[{"ingredient": "spaghetti"", "amount": "10"}]", "category": 1, "price": 100}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X POST https://full-dollar-menu.herokuapp.com/menu'
`

-Output: `{'success': True, 'menu_item_id':id}}`

POST '/menu/categories'
- Adds a category to the API
- Request Arguments: name, ingredients, category, price
- Example:  `curl -i -H "Accept: application/json" -d '{"type": "dinner"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X POST https://full-dollar-menu.herokuapp.com/menu/categories'
`

-Output: `{'success': True, 'category_id':id}}`

DELETE 'menu/categories/(category_id)'
- Deletes a category from the API.
- Returns: An object with a success boolean and deleted category id
- Example: `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X DELETE https://full-dollar-menu.herokuapp.com/menu/categories/1'
`

-Output: `{'success': True, 'category_id':id}}`

DELETE 'menu/(menu_item_id)'
- Deletes a menu_item from the API.
- Returns: An object with a success boolean and deleted menu_item id
- Example: `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X DELETE https://full-dollar-menu.herokuapp.com/menu/1'
`

-Output: `{'success': True, 'menu_item_id':id}}`

PATCH 'menu/(menu_item_id)'
- Edits an attribute or more of a menu_item from the API.
- Returns: An object with a success boolean and edit menu_item list
- Example: `curl -i -H "Accept: application/json" -d '{"name":"Fries"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X PATCH https://full-dollar-menu.herokuapp.com/menu/1'
`

-Output: `{'success': True, "menu_items": []}`

##Error Codes
The error codes utilized are as followed:

- 400 (Bad Request)
- 401 (Unauthorized)
- 404 (Resource Not Found)
- 422 (Unproccessable)

## Testing
To run the tests, run
```
dropdb capstone_test
createdb capstone_test
python test_app.py
```