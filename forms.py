from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Optional, re, ValidationError

class CastingForm(Form):
    actor_id = StringField(
        'actor_id',
        validators=[DataRequired()]
    )
    movie_id = StringField(
        'movie_id',
        validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )
    place = StringField(
        'place',
        validators=[DataRequired()]
    )

def PhoneValidated(form, field):
    if not re.search(r'^[0-9\-\+]+$', field.data):
        raise ValidationError("Phone number is invalid format.")

class MovieForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    producer = StringField(
        'producer', validators=[DataRequired()]
    )
    director = StringField(
        'director', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), PhoneValidated]
    )
    image_link = StringField(
        'image_link', validators=[URL(), Optional()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )
    genres = SelectField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Action', 'Action'),
            ('Horror', 'Horror'),
            ('Drama', 'Drama'),
            ('Sci-Fi', 'Sci-Fi'),
            ('Adventure', 'Adventure'),
            ('Thriller', 'Thriller'),
            ('Mistery', 'Mistery'),
            ('History', 'History'),
            ('Animation', 'Animation'),
            ('Comedy', 'Comedy'),
            ('War', 'War'),
            ('Romance', 'Romance'),
        ]
    )
    website = StringField(
        'website', validators=[URL(), Optional()]
    )
    seeking_actor = BooleanField(
        'seeking_actor'
    )
    seeking_description = StringField(
        'seeking_description'
    )

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = StringField(
        'age', validators=[DataRequired()]
    )
    sex = SelectField(
        'sex', validators=[DataRequired()],
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
        ]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), PhoneValidated]
    )
    genres = SelectField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Action', 'Action'),
            ('Horror', 'Horror'),
            ('Drama', 'Drama'),
            ('Sci-Fi', 'Sci-Fi'),
            ('Adventure', 'Adventure'),
            ('Thriller', 'Thriller'),
            ('Mistery', 'Mistery'),
            ('History', 'History'),
            ('Animation', 'Animation'),
            ('Comedy', 'Comedy'),
            ('War', 'War'),
            ('Romance', 'Romance'),
        ]
    )
    image_link = StringField(
        'image_link', validators=[URL(), Optional()]
    )
    website = StringField(
        'website', validators=[URL(), Optional()]
    )
    seeking_movie = BooleanField(
        'seeking_movie'
    )
    seeking_description = StringField(
            'seeking_description'
     )
