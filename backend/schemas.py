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