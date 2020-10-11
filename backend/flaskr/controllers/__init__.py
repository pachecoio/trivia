from flask import jsonify
from app import app
from schemas import ErrorHandlerSchema
from decorators import marshal_with
from error_handlers import ApiError


@app.errorhandler(ApiError)
@marshal_with(ErrorHandlerSchema())
def handle_invalid_usage(error):
    return error
