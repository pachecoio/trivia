from flask import jsonify, abort
from app import app
from decorators import parse_request, Argument, marshal_with, parse_with
from flaskr.controllers.category_controller import get_categories
from models import Question
from flaskr.repositories.question_repository import QuestionRepository
from flaskr.repositories.category_repository import CategoryRepository
from schemas import QuizCreateSchema, QuestionSchema
from error_handlers import ApiError
from sqlalchemy import not_
import random


question_repository = QuestionRepository()
category_repository = CategoryRepository()

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
    questions = (
        question_repository.query.filter(Question.category_id == category_id)
        .filter(not_(Question.id.in_(question_ids)))
        .all()
    )
    if not questions:
        raise ApiError(message="No questions left, game is over.", status_code=404)
    index = random.randint(0, len(questions) - 1)
    return questions[index]
