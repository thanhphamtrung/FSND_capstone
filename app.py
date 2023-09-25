#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, request, jsonify, abort, render_template
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from forms import *
import sys
from datetime import datetime
from models import setup_db, Movie, Actor, Casting, db
from flask_cors import CORS
from auth import AuthError, requires_auth
import markdown



def create_app(test_config=None):
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    #----------------------------------------------------------------------------#
    # Filters.
    #----------------------------------------------------------------------------#

    def format_datetime(value, format='medium'):
      date = dateutil.parser.parse(value)
      if format == 'full':
          format="EEEE MMMM, d, y 'at' h:mma"
      elif format == 'medium':
          format="EE MM, dd, y h:mma"
      return babel.dates.format_datetime(date, format, locale='en')

    app.jinja_env.filters['datetime'] = format_datetime
    
    ITEMS_PER_PAGE = 10

    def paginate_items(request, selection):
      page = request.args.get("page", 1, type = int)
      start = (page - 1) * ITEMS_PER_PAGE
      end = start + ITEMS_PER_PAGE

      items = [item.format() for item in selection]
      current_items = items[start:end]

      return current_items

    def search_movies(search_term):
      if search_term:
        movies = Movie.query.order_by(Movie.id).filter(
                    Movie.name.ilike("%{}%".format(search_term))
        ).all()

        if len(movies) == 0:
            abort(404)

        current_movies = paginate_items(request, movies)

        return jsonify(
            {
                "success": True,
                "movies": current_movies,
                "total_movies": len(movies),
            }
        )

      abort(400)

    def search_actors(search_term):
      if search_term:
        actors = Actor.query.order_by(Actor.id).filter(
                    Actor.name.ilike("%{}%".format(search_term))
        ).all()

        if len(actors) == 0:
            abort(404)

        current_actors = paginate_items(request, actors)

        return jsonify(
            {
                "success": True,
                "actors": current_actors,
                "total_actors": len(actors),
            }
        )

      abort(400)

    #----------------------------------------------------------------------------#
    # Controllers.
    #----------------------------------------------------------------------------#

    @app.route('/')
    def index():
      readme_file = open("README.md", "r")
      md_template_string = markdown.markdown(
          readme_file.read(), extensions=["fenced_code"]
      )
      return md_template_string

    #  Movies
    #  ----------------------------------------------------------------

    @app.route('/movies')
    @requires_auth('get:movies')
    def movies():
      search_term = request.args.get("searchTerm", "", type = str)
      print(search_term)
      if search_term:
        return search_movies(search_term)

      movies = Movie.query.order_by(Movie.id).all()
      current_movies = []
      if len(movies) > 0:
          current_movies = paginate_items(request, movies)

      if len(current_movies) == 0:
          abort(404)

      return jsonify(
        {
            "success": True,
            "movies": current_movies,
            "total_movies": len(movies),
        }
      )

    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def casting_movie(movie_id):
      movie = Movie.query.get_or_404(movie_id)

      return jsonify(
        {
          'success': True,
          'movie': movie.format()
        }
      )

    #  Create Movie
    #  ----------------------------------------------------------------
    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def create_movie():
      error = False
      errorMsg = ""
      movie_format = {}
      form = MovieForm(request.form, meta={'csrf': False})
      if not form.validate():
        error = True
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        errorMsg = 'Form format error. Please fix the following errors: ' + ', '.join(message)
      else:
        try:
          movie = Movie()
          movie.id = len(Movie.query.all()) + 1
          movie.name = form.name.data
          movie.producer = form.producer.data
          movie.director = form.director.data
          movie.phone = form.phone.data
          movie.image_link = form.image_link.data
          movie.facebook_link = form.facebook_link.data
          movie.website = form.website.data
          movie.seeking_actor = form.seeking_actor.data
          movie.seeking_description = form.seeking_description.data

          genres = request.form.getlist('genres')
          movie.genres = ','.join(genres)

          movie.insert()
          movie_format = movie.format()
        except:
          db.session.rollback()
          error = True
          errorMsg = str(sys.exc_info())
          print(sys.exc_info())
        finally:
          db.session.close()

      
      if error:
        return jsonify(
          {
            'success': False,
            'message': errorMsg
          }
        )

      return jsonify(
        {
          'success': True,
          'movie': movie_format
        }
      )

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
      error = False
      try:
        movie = Movie.query.get(movie_id)
        movie.delete()
      except:
        db.session.rollback()
        error = True
      finally:
        db.session.close()

      if error:
        return jsonify(
          {
            'success': False,
            'message': "An error occurred. Movie could not be deleted."
          }
        )
      else:
        return jsonify(
          {
            'success': True,
            'id': movie_id
          }
        )


    #  Actors
    #  ----------------------------------------------------------------
    @app.route('/actors')
    @requires_auth('get:actors')
    def actors():
      search_term = request.args.get("searchTerm", "", type = str)
      if search_term:
        return search_actors(search_term)

      actors = Actor.query.order_by(Actor.id).all()
      current_actors = []
      if len(actors) > 0:
          current_actors = paginate_items(request, actors)

      if len(current_actors) == 0:
          abort(404)

      return jsonify(
        {
            "success": True,
            "actors": current_actors,
            "total_actors": len(actors),
        }
      )

    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def casting_actor(actor_id):
      actor = Actor.query.get_or_404(actor_id)

      return jsonify(
        {
          'success': True,
          'actor': actor.format()
        }
      )

    #  Update
    #  ----------------------------------------------------------------
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def edit_actor(actor_id):
      error = False
      errorMsg = ""
      actor_format = {}
      form = ActorForm(request.form, meta={'csrf': False})
      if not form.validate():
        error = True
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        errorMsg = 'Form format error. Please fix the following errors: ' + ', '.join(message)
      else:
        try:
          actor = Actor.query.get(actor_id)
          actor.name = form.name.data
          actor.age = form.age.data
          actor.sex = form.sex.data
          actor.city = form.city.data
          actor.state = form.state.data
          actor.phone = form.phone.data
          actor.image_link = form.image_link.data
          actor.website = form.website.data
          actor.seeking_movie = form.seeking_movie.data
          actor.seeking_description = form.seeking_description.data

          genres = request.form.getlist('genres')
          actor.genres = ','.join(genres)
          
          actor_format = actor.format()

          actor.update()
        except:
          db.session.rollback()
          error = True
          errorMsg = str(sys.exc_info())
        finally:
          db.session.close()

      if error:
        return jsonify(
          {
            'success': False,
            'message': errorMsg
          }
        )

      return jsonify(
        {
          'success': True,
          'actor': actor_format
        }
      )

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def edit_movie(movie_id):
      error = False
      errorMsg = ""
      movie_format = {}
      form = MovieForm(request.form, meta={'csrf': False})
      if not form.validate():
        error = True
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        errorMsg = 'Form format error. Please fix the following errors: ' + ', '.join(message)
      else:
        try:
          movie = Movie.query.get(movie_id)
          movie.name = form.name.data
          movie.producer = form.producer.data
          movie.director = form.director.data
          movie.phone = form.phone.data
          movie.image_link = form.image_link.data
          movie.facebook_link = form.facebook_link.data
          movie.website = form.website.data
          movie.seeking_actor = form.seeking_actor.data
          movie.seeking_description = form.seeking_description.data

          genres = request.form.getlist('genres')
          movie.genres = ','.join(genres)

          movie_format = movie.format()

          movie.update()
        except:
          db.session.rollback()
          error = True
          errorMsg = str(sys.exc_info())
        finally:
          db.session.close()

      if error:
        return jsonify(
          {
            'success': False,
            'message': errorMsg
          }
        )

      return jsonify(
        {
          'success': True,
          'movie': movie_format
        }
      )

    #  Create Actor
    #  ----------------------------------------------------------------
    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def create_actor():
      error = False
      errorMsg = ""
      actor_format = {}
      form = ActorForm(request.form, meta={'csrf': False})
      if not form.validate():
        error = True
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        errorMsg = 'Form format error. Please fix the following errors: ' + ', '.join(message)
      else:
        try:
          actor = Actor()
          actor.id = len(Actor.query.all()) + 1
          actor.name = form.name.data
          actor.city = form.city.data
          actor.state = form.state.data
          actor.phone = form.phone.data
          actor.image_link = form.image_link.data
          actor.website = form.website.data
          actor.seeking_movie = form.seeking_movie.data
          actor.seeking_description = form.seeking_description.data

          genres = request.form.getlist('genres')
          actor.genres = ','.join(genres)
          
          actor_format = actor.format()

          db.session.add(actor)
          db.session.commit()
        except:
            db.session.rollback()
            error = True
            errorMsg = str(sys.exc_info())
            print(sys.exc_info())
        finally:
            db.session.close()

      if error:
        return jsonify(
          {
            'success': False,
            'message': errorMsg
          }
        )

      return jsonify(
        {
          'success': True,
          'actor': actor_format
        }
      )

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
      error = False
      try:
        actor = Actor.query.get(actor_id)
        db.session.delete(actor)
        db.session.commit()
      except:
        db.session.rollback()
        error = True
      finally:
        db.session.close()

      if error:
        return jsonify(
          {
            'success': False,
            'message': "An error occurred. Actor could not be deleted."
          }
        )
      else:
        return jsonify(
          {
            'success': True,
            'id': actor_id
          }
        )

    #  Castings
    #  ----------------------------------------------------------------

    @app.route('/castings')
    @requires_auth('get:castings')
    def castings():
      castings = Casting.query.order_by(Casting.id).all()
      current_castings = []
      if len(castings) > 0:
          current_castings = paginate_items(request, castings)

      if len(current_castings) == 0:
          abort(404)

      return jsonify(
        {
            "success": True,
            "castings": current_castings,
            "total_castings": len(castings),
        }
      )

    @app.route('/castings', methods=['POST'])
    @requires_auth('add:castings')
    def create_casting():
      error = False
      errorMsg = ""
      castings_format = {}
      form = CastingForm(request.form, meta={'csrf': False})
      if not form.validate():
        error = True
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        errorMsg = 'Form format error. Please fix the following errors: ' + ', '.join(message)
      else:
        try:
          if Movie.query.get(form.movie_id.data) is None:
            errorMsg = "Movie is not found"
            raise Exception(errorMsg)
          if Actor.query.get(form.actor_id.data) is None:
            errorMsg = "Actor is not found"
            raise Exception(errorMsg)

          casting = Casting()
          casting.id = len(Casting.query.all()) + 1
          casting.movie_id = form.movie_id.data
          casting.actor_id = form.actor_id.data
          casting.start_time = form.start_time.data
          casting.place = form.place.data
          
          castings_format = casting.format()
          casting.insert()
        except:
          db.session.rollback()
          error = True
          errorMsg = str(sys.exc_info())
        finally:
          db.session.close()

      if error:
        return jsonify(
          {
            'success': False,
            'message': errorMsg
          }
        )

      return jsonify(
        {
          'success': True,
          'casting': castings_format
        }
      )

    @app.route('/castings/<casting_id>', methods=['DELETE'])
    @requires_auth('delete:castings')
    def delete_casting(casting_id):
      error = False
      try:
        casting = Casting.query.get(casting_id)
        db.session.delete(casting)
        db.session.commit()
      except:
        db.session.rollback()
        error = True
      finally:
        db.session.close()

      if error:
        return jsonify(
          {
            'success': False,
            'message': "An error occurred. Casting could not be deleted."
          }
        )
      else:
        return jsonify(
          {
            'success': True,
            'id': casting_id
          }
        )

    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }
        ), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "not found"
            }
        ), 404

    @app.errorhandler(500)
    def server_internal_erro(error):
        return jsonify(
            {
                "success": False,
                "error": 500,
                "message": "server internal error"
            }
        ), 500

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error
            }
        ), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
