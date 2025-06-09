import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Cats(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True, default='Not specified')
    breed = Column(String, nullable=True, default='Not specified')
    features = Column(String, default='Not specified')
    shelter_id = Column(Integer, ForeignKey('shelters.id'))

    shelter = relationship('Shelters', backref='cats')
