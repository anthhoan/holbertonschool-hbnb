from abc import ABC, abstractmethod
from app import db
from sqlalchemy.orm import joinedload
from app.models.place import Place


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

"""
SQLAlchemy Repository
"""

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)


    def get_all(self):
        query = db.session.query(self.model)
        if self.model.__name__ == "Place":
            query = query.options(
                joinedload(self.model.reviews_r),
                joinedload(self.model.amenities_r)
            )
        return query.all()

    def update(self, obj_id, update_data):
        obj = self.get(obj_id)
        if not obj:
            return None
        obj.update(update_data)
        db.session.commit()
        return obj 


    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
