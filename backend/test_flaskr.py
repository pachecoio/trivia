import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

CATEGORIES_MOCK = [
    Category(
        type="category 1"
    ),
    Category(
        type="category 2"
    ),
    Category(
        type="category 3"
    ),
    Category(
        type="category 4"
    ),
    Category(
        type="category 5"
    ),
]
QUESTIONS_MOCK = [
    Question(
        question="question 1",
        answer="answer 1",
        difficulty=1,
        category_id=1
    ),
    Question(
        question="question 2",
        answer="answer 2",
        difficulty=5,
        category_id=1
    ),
    Question(
        question="question 3",
        answer="answer 3",
        difficulty=2,
        category_id=2
    ),
    Question(
        question="question 4",
        answer="answer 4",
        difficulty=3,
        category_id=3
    ),
    Question(
        question="question 5",
        answer="answer 5",
        difficulty=1,
        category_id=4
    ),
    Question(
        question="question 6",
        answer="answer 6",
        difficulty=2,
        category_id=5
    ),
]

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "sqlite:///{}.db".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.reflect()
            self.db.drop_all()
        pass

    @property
    def request(self):
        return self.client()

    def _create_category(self, type):
        res = self.request.post("/api/categories", json=dict(type=type))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        return data

    def _get_categories(self):
        res = self.request.get("/api/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        return data

    def _get_questions(self):
        res = self.request.get("/api/questions")
        self.assertEqual(res.status_code, 200)
        return json.loads(res.data)

    def _create_question(self, question):
        data = dict(
            question=question.question,
            answer=question.answer,
            difficulty=question.difficulty,
            category_id=question.category_id,
        )
        res = self.request.post("/api/questions", json=data)
        self.assertEqual(res.status_code, 200)
        return json.loads(res.data)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    """
    Test categories
    """
    def test_get_categories_empty(self):
        data = self._get_categories()
        self.assertEqual(len(data), 0)

    def test_create_category(self):
        type = "Science"
        data = self._create_category(type)
        self.assertEqual(data["type"], type)

    def test_get_categories_success(self):
        # Create categories
        self._create_category(type="Places")
        self._create_category(type="Animals")

        # Make request
        data = self._get_categories()
        self.assertEqual(len(data), 2)


    """
    Test questions
    """
    def test_get_questions_empty(self):
        data = self._get_questions()
        self.assertEqual(len(data.get("categories")), 0)
        self.assertEqual(len(data.get("questions")), 0)
        self.assertEqual(data.get("total_questions"), 0)
        self.assertEqual(data.get("current_category"), None)

    def test_create_questions(self):
        for category in CATEGORIES_MOCK:
            self._create_category(type=category.type)

        questions = []
        for question in QUESTIONS_MOCK:
            q = self._create_question(question)
            questions.append(q)

        self.assertEqual(len(questions), len(QUESTIONS_MOCK))

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()