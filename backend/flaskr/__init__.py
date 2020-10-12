import os
from flask_marshmallow import Marshmallow
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import random
import click
from decorators import parse_request, Argument, marshal_with, parse_with
from flaskr.repositories.category_repository import CategoryRepository
from flaskr.repositories.question_repository import QuestionRepository

from models import setup_db, Question, Category
import click
from schemas import (
    CategorySchema,
    QuestionCollectionSchema,
    QuestionCreateSchema,
    QuestionSchema,
    QuizCreateSchema,
    ErrorHandlerSchema,
)
from error_handlers import ApiError
from sqlalchemy import or_, not_

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.db = setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    Marshmallow(app)
    category_repository = CategoryRepository()
    question_repository = QuestionRepository()

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    """

    @app.route("/api/categories")
    def get_categories():
        categories = category_repository.filter().all()
        return jsonify([category.format() for category in categories])

    @app.route("/api/categories/<int:id>")
    @marshal_with(CategorySchema())
    def get_category(id):
        return category_repository.get(id)

    """
    Cli command to create categories
    """

    @app.cli.command("create_category")
    @click.argument("type")
    def create_category(type):
        category = category_repository.insert(type=type)
        print("Category {} included successfully".format(category.type))

    """
    Cli command to list categories
    """

    @app.cli.command("list_category")
    @click.argument("search")
    def list_category(search=None):
        query = category_repository.filter()
        if search:
            query = query.filter(Category.type.like("%{}%".format(search)))
        categories = query.all()
        print("List categories")
        print("----------------------------------------------------------")
        for category in categories:
            print("id: {}".format(category.id))
            print("type: {}".format(category.type))
            print("---------------------------------------------------------")

    """
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    """

    """
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    """

    """
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    @app.route("/api/questions", methods=["GET"])
    @app.route("/api/categories/<int:current_category>/questions", methods=["GET"])
    @parse_request(
        [
            Argument(name="page", default=0, type=int),
            Argument(name="limit", default=10, type=int),
            Argument(name="search_term", type=str),
        ]
    )
    @marshal_with(QuestionCollectionSchema())
    def get_questions(page=0, limit=10, current_category=None, search_term=None):
        categories = category_repository.filter().all()
        query = question_repository.filter()
        if search_term:
            query = query.filter(
                or_(
                    Question.question.ilike("%{}%".format(search_term)),
                    Question.answer.ilike("%{}%".format(search_term)),
                )
            )
        if current_category:
            query = query.filter(Question.category_id == current_category)
        count = query.count()

        offset = ((page - 1) * limit) + 1 if page > 1 else 0
        questions = query.limit(limit).offset(offset).all()
        return {
            "questions": questions,
            "total_questions": count,
            "categories": categories,
            "current_category": current_category,
        }

    """

    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    """

    @app.route("/api/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        question_repository.delete(id)
        return jsonify({"error": False, "message": "Item delete successfully"}), 202

    """
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    """

    @app.route("/api/questions", methods=["POST"])
    @parse_with(QuestionCreateSchema())
    @marshal_with(QuestionSchema())
    def create_question(entity, *args, **kwargs):
        return question_repository.insert(**entity)

    """
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    """

    @app.route("/api/quizzes", methods=["POST"])
    @parse_with(QuizCreateSchema())
    @marshal_with(QuestionSchema())
    def get_quiz(entity, **kwargs):
        question_ids = entity.get("previous_questions")
        category_id = entity.get("quiz_category")
        query = question_repository.query
        if question_ids:
            query = query.filter(not_(Question.id.in_(question_ids)))
        if category_id:
            query = query.filter(Question.category_id == category_id)
        questions = query.all()
        if not questions:
            raise ApiError(message="No questions left, game is over.", status_code=404)
        index = random.randint(0, len(questions) - 1)
        return questions[index]

    @app.errorhandler(ApiError)
    @marshal_with(ErrorHandlerSchema())
    def handle_invalid_usage(error):
        return error

    return app
