# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Projects(db.Model):

    __tablename__ = 'Projects'

    id = db.Column(db.Integer, primary_key=True)

    #__Projects_FIELDS__
    uuid = db.Column(db.String(255),  nullable=True)
    name = db.Column(db.String(255),  nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Projects_FIELDS__END

    def __init__(self, **kwargs):
        super(Projects, self).__init__(**kwargs)


class Run(db.Model):

    __tablename__ = 'Run'

    id = db.Column(db.Integer, primary_key=True)

    #__Run_FIELDS__
    uuid = db.Column(db.String(255),  nullable=True)
    prompt = db.Column(db.Text, nullable=True)
    prompt_enhanced = db.Column(db.Text, nullable=True)

    #__Run_FIELDS__END

    def __init__(self, **kwargs):
        super(Run, self).__init__(**kwargs)


class Dataset(db.Model):

    __tablename__ = 'Dataset'

    id = db.Column(db.Integer, primary_key=True)

    #__Dataset_FIELDS__
    name_indentified = db.Column(db.String(255),  nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    feedback = db.Column(db.Text, nullable=True)

    #__Dataset_FIELDS__END

    def __init__(self, **kwargs):
        super(Dataset, self).__init__(**kwargs)


class Images(db.Model):

    __tablename__ = 'Images'

    id = db.Column(db.Integer, primary_key=True)

    #__Images_FIELDS__
    uuid = db.Column(db.String(255),  nullable=True)
    filename = db.Column(db.String(255),  nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    error = db.Column(db.Boolean, nullable=True)

    #__Images_FIELDS__END

    def __init__(self, **kwargs):
        super(Images, self).__init__(**kwargs)



#__MODELS__END
