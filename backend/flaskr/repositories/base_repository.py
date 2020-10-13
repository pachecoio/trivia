from flask import jsonify, current_app
from sqlalchemy import exc
from error_handlers import ApiError

class BaseRepository(object):
    name = "BaseRepository"
    
    @property
    def session(self):
        return current_app.db.session

    @property
    def query(self):
        return self.session.query(self.model)

    def get(self, id):
        entity = self.query.get(id)
        if not entity:
            raise ApiError(
                message="{} not found with id {}".format(self.name, id),
                status_code=404,
            )
        return entity

    def filter(self, **kwargs):
        query = self.query
        if kwargs:
            query = query.filter(**kwargs)
        return query

    def insert(self, **kwargs):
        try:
            entity = self.model(**kwargs)
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except:
            raise ApiError(
                message="Error creating new {}".format(self.name),
                status_code=500,
            )

    def update(self, id, **kwargs):
        try:
            entity = self.query.get(id)
            if not entity:
                raise ApiError(
                    message="{} not found with id {}".format(self.name, id),
                    status_code=404,
                )
            for key in kwargs.keys():
                if hasattr(self.model, key):
                    setattr(self.model, key, kwargs.get(key))
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except:
            raise ApiError(
                message="Error updating {}".format(self.name),
                status_code=500,
            )

    def delete(self, id):
        try:
            entity = self.get(id)
            self.session.delete(entity)
            self.session.commit()
            return "", 204
        except:
            raise ApiError(
                message="Error deleting {}".format(self.name),
                status_code=500,
            )
