from typing import List, Iterable

from movies.adapters.repository import AbstractRepository
from movies.domain.allCombined import make_review, Movie, Review, Actor, Director, Genre


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, username: str, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    review = make_review(review_text=review_text, user=user, movie=movie)

    repo.add_review(review)
    return review_to_dict(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def add_to_watchlist(movie_id: int, username: str,  repo: AbstractRepository):

    if repo.get_user(username) is None:
        raise UnknownUserException


    if repo.get_movie(movie_id) is None:
        raise NonExistentMovieException



    repo.add_to_watchlist(repo.get_movie(movie_id), repo.get_user(username))


def remove_from_watchlist(movie_id: int, username: str,  repo: AbstractRepository):
    if repo.get_user(username) is None:
        raise UnknownUserException

    if repo.get_movie(movie_id) is None:
        raise NonExistentMovieException


    repo.remove_from_watchlist(repo.get_movie(movie_id), repo.get_user(username),)


def get_watchlist(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user.watchlist


def get_top_movies(id, repo: AbstractRepository):
    # Returns movies for the target id (empty if no matches), the id of the previous movie (might be null), the id of the next movie (might be null)
    listid = [id]
    movies = repo.get_movies_by_id(listid)

    movies_dto = list()
    prev_id = next_id = None

    if len(movies) > 0:
        prev_id = repo.get_id_of_previous_movie(movies[0])
        next_id = repo.get_id_of_next_movie(movies[0])

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_id, next_id


def get_movie_ids_for_actor(actor_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_actor(actor_name)

    return movie_ids


def get_movie_ids_for_director(director_name, repo: AbstractRepository):
    director_ids = repo.get_movie_ids_for_director(director_name)

    return director_ids


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    genre_ids = repo.get_movie_ids_for_genre(genre_name)

    return genre_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'year': movie.year,
        'title': movie.title,
        'reviews': reviews_to_dict(movie.reviews),
        'actors': movie.actors,
        'director': movie.director,
        'genres': movie.genres,
        "description": movie.description,
        "imagelink": movie.imagelink
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.username,
        'movie_id': review.movie.id,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]



# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.year)
    movie.add_id(dict.id)
    return movie
