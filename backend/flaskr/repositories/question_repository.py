from flaskr.repositories import BaseRepository
from models import Question


class QuestionRepository(BaseRepository):
    model = Question