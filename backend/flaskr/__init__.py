import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
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
    CORS(app)

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
            'total_questions': len(selection),
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

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            if not('question' in body and 'answer' in body and 'difficulty'in body and 'category' in body):
                abort(400)
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)

            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        if search_term:
            questions = Question.query.filter(
                func.lower(Question.question).like('%'+search_term.lower()+"%")
            ).all()
            formatted = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formatted,
                'total_questions': len(questions),
                'current_category': None,
            })
        else:
            abort(404)

    @app.route('/categories/<int:category_id>/questions')
    def get_by_querry(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id
            ).order_by(Question.id).all()
            if len(questions) == 0:
                abort(404)
            formated = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'total_questions': len(questions),
                'current_category': category_id,
                'questions': formated
            })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(400)
            
            category = body.get('quiz_category')
            previous = body.get('previous_questions',None)
            
            if previous :
                
                if category['id']==0:
                    available_questions = Question.query.filter(
                        Question.id.notin_(previous),
                    ).all()
                    
                else:
                    available_questions = Question.query.filter(
                        Question.id.notin_(previous),
                        Question.category == category['id']
                    ).all()
                    
            else:
                
                if category['id']==0:
                    available_questions = Question.query.all()
                else:
                    available_questions = Question.query.filter(
                        Question.category == category['id'],
                    ).all()
            
            if len(available_questions) > 0:
                new_question = available_questions[random.randint(0, len(available_questions))].format()
                  
            else:
                new_question = None
            
            return jsonify({
                'success': True,
                'question': new_question,
            })
        except:
            abort(422)

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

    return app