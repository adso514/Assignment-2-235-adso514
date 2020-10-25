from datetime import date

import pytest

from flix.authentication.services import AuthenticationException
from flix.movies import services as movie_library_services
from flix.authentication import services as auth_services
from flix.movies.services import NonExistentMovieException
from flix.domain.model1 import Movie, Genre, Director, Actor, Review, User


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    auth_services.add_user("thorke", "Copycat112", in_memory_repo)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user('thorke', "abcd1A23", in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    new_username = 'adso514'
    new_password = 'abcdA123'
    auth_services.add_user(new_username, new_password, in_memory_repo)

    movie_id = 3
    review_text = 'Average movie'

    # Call the service layer to add the review.
    movie_library_services.add_review(movie_id, review_text, new_username, in_memory_repo)

    # Retrieve the review for the movie from the repository.
    reviews_as_dict = movie_library_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the review includes a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 1001
    review_text = "good film"
    new_username = 'adso514'
    new_password = 'Copycat112'
    auth_services.add_user(new_username, new_password, in_memory_repo)

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_library_services.NonExistentMovieException):
        movie_library_services.add_review(movie_id, review_text, new_username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 54
    review_text = 'Good acting'
    username = 'adso514'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movie_library_services.UnknownUserException):
        movie_library_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 1

    movie_as_dict = movie_library_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['year'] == 2014
    assert movie_as_dict['title'] == 'Guardians of the Galaxy'
    assert movie_as_dict['description'] == ('A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.')
    assert len(movie_as_dict['reviews']) == 0
    assert movie_as_dict['actors'] == [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper"),
                            Actor("Zoe Saldana")]
    assert movie_as_dict['genres'] == [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]
    assert movie_as_dict['director'] == Director("James Gunn")


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 1002

    # Call the service layer to attempt to retrieve the movie.
    with pytest.raises(movie_library_services.NonExistentMovieException):
        movie_library_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_library_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_library_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1000


def test_get_movies_by_rank_with_one_rank(in_memory_repo):
    target_id = 75

    movies_as_dict, prev_id, next_id = movie_library_services.get_movies_by_rank(target_id, in_memory_repo)

    assert len(movies_as_dict) == 1
    assert movies_as_dict[0]['id'] == 75

    assert prev_id == 74
    assert next_id == 76


def test_get_movies_by_id_with_non_existent_id(in_memory_repo):
    target_id = 1111

    movies_as_dict, prev_date, next_date = movie_library_services.get_movies_by_rank(target_id, in_memory_repo)

    # Check that there are no movies with id 1100
    assert len(movies_as_dict) == 0


def test_get_movies_by_multiple_id(in_memory_repo):
    target_movie_ids = [1, 2, 11111, 22222]
    movies_as_dict = movie_library_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the movie ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([1, 2]).issubset(movie_ids)


def test_get_reviews_for_movie(in_memory_repo):
    movie_id = 1
    review_text = "Good as movie"
    new_username = 'adso514'
    new_password = 'cOPYCAT112'
    auth_services.add_user(new_username, new_password, in_memory_repo)
    movie_library_services.add_review(movie_id, review_text, new_username, in_memory_repo)

    reviews_as_dict = movie_library_services.get_reviews_for_movie(1, in_memory_repo)
    assert len(reviews_as_dict) == 1

    # Check that the review relates to the movie whose id is 1.
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movie_library_services.get_reviews_for_movie(1001, in_memory_repo)


def test_get_review_for_movie_without_review(in_memory_repo):
    reviews_as_dict = movie_library_services.get_reviews_for_movie(1, in_memory_repo)
    assert len(reviews_as_dict) == 0

