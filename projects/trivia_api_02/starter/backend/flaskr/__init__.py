import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from backend.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, question_selection):
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in question_selection]
    paginated_questions = questions[start:end]

    return paginated_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={'/': {'origins': '*'}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route("/categories", methods=['GET'])
    def get_categories():
        selection = Category.query.all()
        if len(selection) == 0:
            abort(404)
        categories = {category.id: category.type for category in selection}
        return jsonify({
          'success': True,
          'categories': categories#[category.format() for category in selection],

        })
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route("/questions", methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        category_selection = Category.query.all()
        categories = {category.id: category.type for category in category_selection}
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categories

        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'question_id': question_id

            })
        except Exception as error:
            abort(422)
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route("/questions", methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question_string = body.get('question', None)
        new_answer_string = body.get('answer', None)
        new_category_string = body.get('category', None)
        new_difficulty_string = body.get('difficulty', None)

        try:
            new_question = Question(question=new_question_string, answer=new_answer_string,
                                    category=new_category_string, difficulty=new_difficulty_string)
            new_question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
              'success': True,
              'created': new_question.id,
              'questions': current_questions,
              'total_questions': len(Question.query.all())

            })
        except Exception as error:
            abort(422)
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            phrase = body.get('SearchTerm')
            selection = Question.query.filter(Question.question.ilike("%{}%".format(phrase))).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': len(current_questions)
            })
        except Exception:
            abort(422)
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def get_questions_by_category(category_id):
        selection = Question.query.filter(Question.category == category_id).all()
        current_questions = paginate_questions(request, selection)

        if len(selection) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'category': category_id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())

        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            body = request.get_json()

            previous_questions = body.get('previous_questions')
            category = body.get('quiz_category')

            def get_random_question(questions):
                return questions[random.randint(0, len(questions)-1)]
            category_id = category['id']
            if int(category_id) == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == int(category_id)).all()


            if len(previous_questions) == len(questions):
                return jsonify({
                    'success': True
                        })

            question = get_random_question(questions)
            while question in questions:
                question = get_random_question(questions)

            print(question.format())
            return jsonify({
                "success": True,
                "question": question.format()
            })
        except Exception:
            abort(400)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unproccessable'
        }), 422

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
