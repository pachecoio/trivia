from flask import jsonify
import click
from app import app
from decorators import parse_request, Argument, marshal_with
from flaskr.repositories.category_repository import CategoryRepository
from models import Category
from schemas import CategorySchema


repository = CategoryRepository()

"""
@TODO: 
Create an endpoint to handle GET requests 
for all available categories.
"""


@app.route("/api/categories")
def get_categories():
    categories = repository.filter().all()
    return jsonify([category.format() for category in categories])


@app.route("/api/categories/<int:id>")
@marshal_with(CategorySchema())
def get_category(id):
    return repository.get(id)


"""
Cli command to create categories
"""


@app.cli.command("create_category")
@click.argument("type")
def create_category(type):
    category = repository.insert(type=type)
    print("Category {} included successfully".format(category.type))


"""
Cli command to list categories
"""


@app.cli.command("list_category")
@click.argument("search")
def list_category(search=None):
    query = repository.filter()
    if search:
        query = query.filter(Category.type.like("%{}%".format(search)))
    categories = query.all()
    print("List categories")
    print("----------------------------------------------------------")
    for category in categories:
        print("id: {}".format(category.id))
        print("type: {}".format(category.type))
        print("---------------------------------------------------------")