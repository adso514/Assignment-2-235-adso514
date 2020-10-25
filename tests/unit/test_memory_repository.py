from datetime import date, datetime
from typing import List

import pytest

from flix.domain.model1 import Movie, Genre, Director, Actor, Review, make_review, User
from flix.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 Articles.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        "Life of Pi",
        2020
    )
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(1001) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    # Check that the movie has the expected title.
    assert movie.title == 'The Invitation'
    assert movie.genres == [Genre("Drama"), Genre("Mystery"), Genre("Thriller")]
    assert movie.director == Director("Karyn Kusama")
    assert movie.actors == [Actor("Logan Marshall-Green"), Actor("Emayatzy Corinealdi"), Actor("Michiel Huisman"), Actor("Tammy Blanchard")]
    assert movie.year == 2015
    assert len(movie.reviews) == 0

def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie('Flight of the bumblebees')
    assert movie is None


def test_repository_can_retrieve_movies_by_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2014)

    assert len(movies) == 98


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(1745)
    assert len(movies) == 0


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Nine Lives'


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([3, 21, 31])

    assert len(movies) == 3
    assert movies[
               0].title == 'Split'
    assert movies[1].title == "Gold"
    assert movies[2].title == 'Why Him?'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 162, 1001])

    assert len(movies) == 1
    assert movies[
               0].title == 'Free Fire'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 5000])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_actor(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_actor('Tom Cruise')
    movie_ids.sort()
    assert movie_ids == [201, 234, 276, 434, 537, 870, 973, 164]


def test_repository_returns_an_empty_list_for_non_existent_actor(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_actor('Angelo DSouza')

    assert len(movie_ids) == 0

def test_repository_returns_movie_ids_for_existing_director(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_director('Christopher Nolan')
    movie_ids.sort()
    assert movie_ids == [37, 55, 65, 81, 125]


def test_repository_returns_an_empty_list_for_non_existent_director(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_director('Angelo DSouza')

    assert len(movie_ids) == 0

def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('War')
    movie_ids.sort()
    assert movie_ids == [78, 114, 161, 187, 231, 241, 480, 511, 644, 714, 763, 821, 895]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('Animal')

    assert len(movie_ids) == 0


def test_repository_can_add_a_review(in_memory_repo):
    user = User('Angelo', '123456789')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('Angelo')
    movie = in_memory_repo.get_movie(2)
    review = make_review(review_text="This movie was average", user=user, movie= movie)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "terrible")

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(in_memory_repo):
    user = User('Angelo', '123456789')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('Angelo')
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "terrible movie")

    user.add_review(review)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 0
    user = User('Angelo', '123456789')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('Angelo')
    movie = in_memory_repo.get_movie(2)
    review = make_review(review_text="Very good movie", user=user, movie=movie)

    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_reviews()) == 1


