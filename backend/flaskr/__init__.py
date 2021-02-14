import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    """
    A helper function that helps divide the questions fetched from the
    database into pages
    Arguments:
    ----------
    selection: the data to select from
    request: the request object
    """
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = [question.format() for question in selection]
    return current_questions[start:end]


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Intiate CORS
    CORS(app, resources={'/': {'origins': '*'}})

    # After request headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response

    @app.route("/categories")
    def get_categories():
        current_categories = Category.query.order_by(Category.id).all()
        if len(current_categories) == 0:
            abort(404)
        formated_categories = {
            category.id: category.type for category in current_categories
        }
        return jsonify({
            'success': True,
            'categories': formated_categories
        })

    @app.route('/questions')
    def get_questions_paginated():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions_number': len(selection),
            'current_category': None,
            'categories': {
                category.id: category.type for category in categories
            }
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question.id
            })

        except:
            abort(422)

    '''
        @TODO: 
        Create an endpoint to POST a new question, 
        which will require the question and answer text, 
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab, 
        the form will clear and the question will appear 
        at the end of the last page
        of the questions list in the "List" tab.  
    '''

    '''
        @TODO: 
        Create a POST endpoint to get questions based on a search term. 
        It should return any questions for whom the search term 
        is a substring of the question. 

        TEST: Search by any phrase. The questions list will update to include 
        only question that include that string within their question. 
        Try using the word "title" to start. 
    '''

    '''
        @TODO: 
        Create a GET endpoint to get questions based on category. 

        TEST: In the "List" tab / main screen, clicking on one of the 
        categories in the left column will cause only questions of that 
        category to be shown. 
    '''


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

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(422)
    def cannot_process(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Request cannot be procesed'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app

    
