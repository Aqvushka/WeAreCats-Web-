import datetime
from email.policy import default
from enum import unique

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Shelters(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'shelters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True)
    address = Column(String, nullable=True)
    validated = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('Users', backref='shelters')
