from flask import jsonify
from app import app
from sqlalchemy import exc


class BaseRepository(object):
    @property
    def session(self):
        return app.db.session

    @property
    def query(self):
        return self.session.query

    def filter(self, **kwargs):
        query = self.query(self.model)
        if kwargs:
            query = query.filter(**kwargs)
        return query

    def insert(self, **kwargs):
        entity = self.model(**kwargs)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, id, **kwargs):
        entity = self.query.get(id)
        if not entity:
            return jsonify(
                {"error": True, "message": "Entity not found with id {}".format(id)}
            ), 404
        for key in kwargs.keys():
            if hasattr(self.model, key):
                setattr(self.model, key, kwargs.get(key))
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, id):
        entity = self.query.get(id)
        if not entity:
            return jsonify(
                {"error": True, "message": "Entity not found with id {}".format(id)}
            ), 404
        self.session.delete(entity)
        self.session.commit()
        return "", 204