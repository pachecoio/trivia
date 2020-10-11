from flask import jsonify
from app import app
from schemas import ErrorHandlerSchema
from decorators import marshal_with
from error_handlers import ApiError
import flaskr.controllers.category_controller as category_controller
import flaskr.controllers.question_controller as question_controller
import flaskr.controllers.quiz_controller as quiz_controller


@app.errorhandler(ApiError)
@marshal_with(ErrorHandlerSchema())
def handle_invalid_usage(error):
    return error


__all__ = ["category_controller", "question_controller", "quiz_controller"]
