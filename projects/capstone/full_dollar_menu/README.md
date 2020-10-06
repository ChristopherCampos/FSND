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

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to run the flask application.

The link associated for my specific project is https://chris-campos.us.auth0.com/authorize?audience=fdm&response_type=token&client_id=3dAm6kZYfeaCxH6ehGUHR3V6MMrbXlj0&redirect_uri=http://0.0.0.0:8080/menu/
## API Reference
Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Example: `curl http://127.0.0.1:5000/categories`
-Output: `{'success': True, "categories": {'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}}`

GET '/questions'
- Fetches a list of questions with answers, difficulty, and category id
- Request Arguments: None
- Example: `curl http://127.0.0.1:5000/questions`
-Output: `{'success': True, 'question': {'question' : "How long is the trip from LA to SF?",
'answer' : "a long time",
'category' : 1,
difficulty : 3,
"id": 1
}, "totalQuestions": 1, "categories":{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}}`}`

POST '/questions'
- Adds a question to the API
- Request Arguments: question, answer, difficulty, category
- Returns: An object with a the question, total questions, success message and the created question id
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d 
'{"question": "How long is the sentence?", "answer" : "A sentence long", "difficulty": 2, "category": 1"}`

- Output: `{'success' : True,
"created": 1, "questions": "{"question": "How long is the sentence?", "answer" : "A sentence long", "difficulty": 2, "category": 1", "id": 1}, "total_questions": 1}`
`

DELETE '/questions/(question_id)'
- Deletes a question from the API.
- Returns: An object with a success boolean and deleted question id
- Example: `curl http://127.0.0.1:5000/questions/1 -X DELETE`
-Output: `{"success" True, "deleted": 1}`

POST '/questions/search'
- Fetches a dictionary of categories in which the search phrase is similar to the question.
- Request Arguments: Phrase
- Returns: An object with one or several questions found.
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "California"}`
- Output: `{
              'success': True,
              'questions': {"question": "How long is the sentence?", "answer" : "A sentence long", "difficulty": 2, "category": 1, "id": 1},
              'total_questions': 1
            }`
            
GET '/categories/(int:id)/questions'
- Fetches a dictionary of questions within said category.
- Request Arguments: None
- Returns: An object with one or several questions found.
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "California"}`
- Output: `
            'success': True,
            'category': 1,
            'questions':  {"question": "How large is California?", "answer" : "Big Enough", "difficulty": 2, "category": 1, "id": 1},
            'total_questions': 1)
            }`            
            
POST '/quizzes'
- Fetches a new question for the user to answer based on previous answers.
- Request Arguments: Previous answers, category
- Returns: An object with one new questions in the specified category.
- Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1], "quiz_category": {"type": "Science", "id": "1"}}`
- Output: `{
       "success": True
      "question": {
          "question": "What time zone is California in?"
          "answer": "Pacific Daylight Time", 
          "category": 1, 
          "difficulty": 4, 
          "id": 4, 
      }, 
      "success": true
  }
`
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
python test_flaskr.py
```