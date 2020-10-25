from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, flash

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, Form, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

import movies.adapters.repository as repo
import movies.movie.movie as movie_selection
import movies.search.services as services

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search = MovieSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search.data['search'], search.data['select'])

    return render_template('search/search.html', form=search, title="Search a movie either by actor, director or genre", description="Search for movies by actor, genre or director")


@search_blueprint.route('/results')
def search_results(search, select):
    search = search.title()
    search_exists = services.search_exists(search.title(), select, repo.repo_instance)
    if search_exists:
        if select == "Actor":
            return redirect(url_for('movie_bp.movies_by_actor', actor=search.title()))

        elif select == "Director":
            return redirect(url_for('movie_bp.movies_by_director', director=search.title()))
        elif select == "Genre":
            return redirect(url_for('movie_bp.movies_by_genre', genre=search.title()))
    else:
        flash('No results found, Please search again')
        return redirect(url_for('search_bp.search'))


 

class MovieSearchForm(Form):
    choices = [('Actor', 'Actor'),
               ('Director', 'Director'),
               ('Genre', 'Genre')]
    select = SelectField('Search for movie:', choices=choices)
    search = StringField('')

