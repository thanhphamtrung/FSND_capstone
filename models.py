import os
from sqlalchemy_utils import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    if not database_exists(database_path):
      create_database(database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    producer = db.Column(db.String)
    director = db.Column(db.String)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres =  db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_actor = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))
    castings = db.relationship('Casting', backref='movie', lazy='joined', cascade="all, delete")

    def update(self, d = None):
      if d is not None:
        genres = d.getlist('genres')
        self.genres = ','.join(genres)
        for key, value in d.items():
          if key != "genres":
            setattr(self, key, value)
      db.session.commit()

    def insert(self, d = None):
      if d is not None:
        genres = d.getlist('genres')
        self.genres = ','.join(genres)
        for key, value in d.items():
          if key != "genres":
            setattr(self, key, value)
      db.session.add(self)
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
        return {
          'id':self.id,
          'name':self.name,
          'producer':self.producer,
          'director':self.director,
          'phone':self.phone,
          'image_link':self.image_link,
          'facebook_link':self.facebook_link,
          'genres':self.genres,
          'website':self.website,
          'seeking_actor':self.seeking_actor,
          'seeking_description':self.seeking_description
        }

class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer, db.CheckConstraint('age > 0 AND age < 100'))
    sex = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres =  db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    seeking_movie = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))
    castings = db.relationship('Casting', backref='actor', lazy='joined', cascade="all, delete")

    def update(self, d = None):
      if d is not None:
        genres = d.getlist('genres')
        self.genres = ','.join(genres)
        for key, value in d.items():
          if key != "genres":
            setattr(self, key, value)
      db.session.commit()

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
        return {
          'id':self.id,
          'name':self.name,
          'age':self.age,
          'sex':self.sex,
          'city':self.city,
          'state':self.state,
          'phone':self.phone,
          'genres':self.genres,
          'image_link':self.image_link,
          'website':self.website,
          'seeking_movie':self.seeking_movie,
          'seeking_description':self.seeking_description
        }

class Casting(db.Model):
    __tablename__ = 'Casting'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    start_time = db.Column(db.TIMESTAMP)
    place = db.Column(db.String)

    def update(self):
      db.session.commit()

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'movie_id': self.movie_id,
          'actor_id': self.actor_id,
          'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
          'place': self.place
        }