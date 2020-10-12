from flaskr.repositories import BaseRepository
from models import Question


class QuestionRepository(BaseRepository):
    name = "Question"
    model = Question