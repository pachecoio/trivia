from flaskr import create_app

app = create_app()


# Setup controllers
from flaskr.controllers.category_controller import *
from flaskr.controllers.question_controller import *
from flaskr.controllers.quiz_controller import *

app.run()