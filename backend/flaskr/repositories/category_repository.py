from flaskr.repositories import BaseRepository
from models import Category


class CategoryRepository(BaseRepository):
    name = "Category"
    model = Category