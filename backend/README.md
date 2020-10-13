# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints


### GET '/categories'
- Fetches a list of categories
- Request Arguments: None
- Returns: A list of category objects with two keys: id and type
```
[
  {
    "id": 1,
    "type: "Science",
  },
  {
    "id": 2,
    "type: "Art",
  }
]
```

### GET '/api/categories/<int:id>'
- Fetches a single category by id
- Request Arguments: id
- Returns: A category object with two keys: id and type
```
{
  "id": 1,
  "type: "Science",
}
```

### POST '/api/categories'
- Creates a new category
- Request Arguments: None
- Request body: 
  - Type: json
  - Content:
 ```
{
  "type: "Science",
}
 ```
- Returns: A category object with two keys: id and type
```
{
  "id": 1,
  "type: "Science",
}
```

### GET '/api/questions'
- Fetches a list of questions
- Request Arguments: None
- Request Params:
  - page:
    - required: False
    - type: Integer
  - limit:
    - required: False
    - type: Integer
  - search_term:
    - required: False
    - type: String
- Returns: A list an object with list the result questions based on the search, all categories, current category and total questions.
```
{
  "categories": [
    {
      "id": 1,
      "type": "Movies"
    }
  ],
  "current_category": {
    "id": 1,
    "type": "Movies"
  },
  "questions": [
    {
      "answer": "answer",
      "category": {
        "id": 1,
        "type": "Movies"
      },
      "difficulty": 1,
      "id": 1,
      "question": "question"
    }
  ],
  "total_questions": 0
}
```

### POST '/api/questions'
- Creates a new question
- Request Arguments: None
- Request body: 
  - Type: json
  - Content:
 ```
{
	"question": "question",
	"answer": "answer",
	"difficulty": 1,
	"category_id": 1
}
 ```
- Returns: A question object with two keys: id, question, answer, category and difficulty
```
{
  "answer": "answer",
  "category": {
    "id": 1,
    "type": "Movies"
  },
  "difficulty": 1,
  "id": 1,
  "question": "question"
}
```

### DELETE '/api/questions/<int:id>'
- Deletes a question
- Request Arguments: id
- Returns: A category object with two keys: id and type
```
{
  "id": 1,
  "error": false,
  "message": "Item deleted successfully"
}
```

### POST '/api/quizzes'
- Creates a new quiz
- Request Arguments: None
- Request body: 
  - Type: json
  - Content:
 ```
{
	"previous_questions": [
    2, 3
  ],
	"quiz_category": 1
}
 ```
- Returns: A question object with two keys: id, question, answer, category and difficulty.
This endpoint returns a question that DOES NOT have the ID equal to one of the `previous_questions` ids passed and it also has to have a `category_id` equal to the one requested.
If the `quiz_category` value is equal to 0, it returns all existing questions.
```
{
  "answer": "answer",
  "category": {
    "id": 1,
    "type": "Movies"
  },
  "difficulty": 1,
  "id": 3,
  "question": "question"
}
```

## Error Handling

Errors are returned as JSON objects in the following format:
```
{
  "error": true,
  "message": "Item not found",
  "status_code": 404
}
```

The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Server Error


## Testing
To run the tests, run
```
python test_flaskr.py
```