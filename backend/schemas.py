from app import app
from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow(app)


class CategorySchema(ma.Schema):
    id = fields.Integer()
    type = fields.String()

class QuestionSchema(ma.Schema):
    id = fields.Integer()
    question = fields.String()
    answer = fields.String()
    caregory_id = fields.Integer()
    category = fields.Nested(CategorySchema)
    difficulty = fields.Integer()

class QuestionCollectionSchema(ma.Schema):
    questions = fields.List(
        fields.Nested(QuestionSchema)
    )
    total_questions = fields.Integer()
    categories = fields.List(
        fields.Nested(CategorySchema)
    )
    current_category = fields.String()

class QuestionCreateSchema(ma.Schema):
    question = fields.String()
    answer = fields.String()
    category_id = fields.Integer()
    difficulty = fields.Integer()


class QuizCreateSchema(ma.Schema):
    previous_questions = fields.List(fields.Integer())
    quiz_category = fields.Integer(attribute="quiz_category")


class ErrorHandlerSchema(ma.Schema):
    error = fields.Boolean(default=True)
    status_code = fields.Integer()
    message = fields.String()