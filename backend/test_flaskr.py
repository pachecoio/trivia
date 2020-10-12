import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

CATEGORIES_MOCK = [
    Category(type="category 1"),
    Category(type="category 2"),
    Category(type="category 3"),
    Category(type="category 4"),
    Category(type="category 5"),
]
QUESTIONS_MOCK = [
    Question(question="question 1", answer="answer 1", difficulty=1, category_id=1),
    Question(question="question 2", answer="answer 2", difficulty=5, category_id=1),
    Question(question="question 3", answer="answer 3", difficulty=2, category_id=2),
    Question(question="question 4", answer="answer 4", difficulty=3, category_id=3),
    Question(question="question 5", answer="answer 5", difficulty=1, category_id=4),
    Question(question="question 6", answer="answer 6", difficulty=2, category_id=5),
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
        return self.request.post("/api/questions", json=data)

    def _create_quiz(self, previous_questions=[], quiz_category=0):
        return self.request.post(
            "/api/quizzes",
            json=dict(
                previous_questions=previous_questions, quiz_category=quiz_category
            ),
        )

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

    def test_create_categories(self):
        categories = []
        for category in CATEGORIES_MOCK:
            c = self._create_category(type=category.type)
            categories.append(c)
        self.assertEqual(len(categories), len(CATEGORIES_MOCK))
        for index, category in enumerate(categories):
            self.assertEqual(category["type"], CATEGORIES_MOCK[index].type)

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

    def test_create_question_category_does_not_exists(self):
        INVALID_ID = 100
        res = self._create_question(
            Question(
                question="Question fail",
                answer="answer fail",
                difficulty=1,
                category_id=INVALID_ID,
            )
        )
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(
            data["message"], "Category not found with id {}".format(INVALID_ID)
        )

    def test_create_questions(self):
        for category in CATEGORIES_MOCK:
            self._create_category(type=category.type)

        questions = []
        for question in QUESTIONS_MOCK:
            res = self._create_question(question)
            self.assertEqual(res.status_code, 200)
            q = json.loads(res.data)
            questions.append(q)

        self.assertEqual(len(questions), len(QUESTIONS_MOCK))

        for index, question in enumerate(questions):
            self.assertEqual(question["question"], QUESTIONS_MOCK[index].question)
            self.assertEqual(question["answer"], QUESTIONS_MOCK[index].answer)
            self.assertEqual(question["difficulty"], QUESTIONS_MOCK[index].difficulty)

    def test_get_quiz_empty(self):
        res = self._create_quiz()
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["message"], "No questions left, game is over.")

    def test_get_quiz_category_all(self):
        # Generate mock categories
        for category in CATEGORIES_MOCK:
            self._create_category(type=category.type)
        # Generate mock questions
        for question in QUESTIONS_MOCK:
            self._create_question(question)

        previous_questions = []
        # Create 3 quizzes and test them
        for n in range(2):
            # Execute request
            res = self._create_quiz(previous_questions=previous_questions)
            # Validate response success
            self.assertEqual(res.status_code, 200)
            data = json.loads(res.data)
            # Validate response=
            self.assertNotIn(data["id"], previous_questions)
            previous_questions.append(data["id"])

    def test_get_quiz_category_1(self):
        # Generate mock categories
        for category in CATEGORIES_MOCK:
            self._create_category(type=category.type)
        # Generate mock questions
        for question in QUESTIONS_MOCK:
            self._create_question(question)

        previous_questions = []
        # Create 3 quizzes and test them
        for n in range(2):
            # Execute request
            res = self._create_quiz(
                previous_questions=previous_questions, quiz_category=1
            )
            # Validate response success
            self.assertEqual(res.status_code, 200)
            data = json.loads(res.data)
            # Validate response=
            self.assertNotIn(data["id"], previous_questions)
            self.assertEqual(data["category"]["id"], 1)
            previous_questions.append(data["id"])

    def test_get_quiz_category_does_not_exist(self):
        INVALID_ID = 100
        res = self._create_quiz(quiz_category=INVALID_ID)
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(
            data["message"], "Category not found with id {}".format(INVALID_ID)
        )


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()