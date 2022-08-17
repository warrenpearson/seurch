import uuid

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Union

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, types
from sqlalchemy.sql import func

db = SQLAlchemy()


@dataclass
class BaseMixin(object):
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at: datetime = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    active: bool = db.Column("active", db.Boolean, nullable=False, default=True)

    @classmethod
    def get(cls, obj_id: Union[int, str, uuid.UUID]) -> Any:
        return cls.query.get(obj_id)

    @classmethod
    def find_by(cls, **kwargs):
        filters = cls._filters(kwargs)
        return db.session.execute(db.select(cls).where(*filters)).scalars().first()

    @classmethod
    def _filters(cls, kwargs):
        return [getattr(cls, attr) == kwargs[attr] for attr in kwargs]

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_if_exists(cls, **kwargs):
        filters = cls._filters(kwargs)
        cls.query.filter(*filters).delete()
        db.session.commit()


class IntEnum(types.TypeDecorator):
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)
