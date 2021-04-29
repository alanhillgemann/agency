import os
import re
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']
# SQLAlchemy 1.4.x workaround:
# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Base(db.Model):
    __abstract__ = True

    def __repr__(self):
        return str(self.__dict__)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    gender = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    movies = relationship(
        "Performance", back_populates="actor", cascade='delete')

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    release_date = Column(DateTime, nullable=False)
    actors = relationship(
        "Performance", back_populates="movie", cascade='delete')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Performance(Base):
    __tablename__ = 'performances'
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    actor = relationship("Actor", back_populates="movies")
    movie = relationship("Movie", back_populates="actors")

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def format(self):
        return {
            'id': self.id,
            'actor_id': self.actor_id,
            'movie_id': self.movie_id
        }
