import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from movies.adapters.repository import AbstractRepository, RepositoryException
from movies.domain.allCombined import Movie, Genre, Director, Actor, Review, User


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list()
        self._movies_index = dict() 
        self._actors = list()
        self._users = list()
        self._genres = list()
        self._directors = list()
        self._reviews = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        if movie.id is None:
            movie.add_id(len(self._movies) + 1)
        insort_left(self._movies, movie)
        self._movies_index[int(movie.id)] = movie

        for genre in movie.genres:
            if genre not in self._genres:
                self._genres.append(genre)

        if movie.director is not None:
            if movie.director not in self._directors:
                self._directors.append(movie.director)

        for actor in movie.actors:
            if actor not in self._actors:
                self._actors.append(actor) 
                
    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  

        return movie           

    def add_to_watchlist(self, movie: Movie, user: User):
        if movie not in user.watchlist:
            user.add_to_watchlist(movie)

    def remove_from_watchlist(self, movie: Movie, user: User):
        if movie in user.watchlist:
            user.remove_from_watchlist(movie)

    

    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        

        matching_movies = list()
        for movie in self._movies:
            if movie.year == target_year:
                matching_movies.append(movie) 
                
            

        return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None
        if len(self._movies) > 0:
            movie = self._movies_index[1]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies_index[len(self._movies)]
        return movie

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Movie ids in the repository.
        existing_ids = [] 
        for id in id_list:
            if id in self._movies_index:
                existing_ids.append(id)
        

        # Fetch the Articles.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def get_movie_ids_for_actor(self, actor_name: str):
        # Linear search, to find the first occurrence of a Actor with the name actor_name.
        actor = next((actor for actor in self._actors if actor.actor_full_name == actor_name), None)

        # Retrieve the ids of movie_library associated with the actor.
        movie_ids = []
        if actor is not None:
            for movie in self._movies:
                if actor in movie.actors:
                    movie_ids.append(movie.id)

        return movie_ids

    def get_movie_ids_for_director(self, director_name: str):
        # Linear search, to find the first occurrence of a Director with the name director_name.
        director = next((director for director in self._directors if director.director_full_name == director_name), None)

        # Retrieve the ids of movie_library associated with the actor.
        movie_ids = []
        if director is not None:
            for movie in self._movies:
                if director == movie.director:
                    movie_ids.append(movie.id)

        return movie_ids

    def get_movie_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Genre with the name genre_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of movie_library associated with the actor.
        movie_ids = []
        if genre is not None:
            for movie in self._movies:
                if genre in movie.genres:
                    movie_ids.append(movie.id)

        return movie_ids


    def get_id_of_previous_movie(self, movie: Movie):
        previous_id = None
        if movie.id != 1:
            previous_id = movie.id - 1
        return previous_id

    def get_id_of_next_movie(self, movie: Movie):
        next_id = None
        if movie.id != len(self._movies):
            next_id = movie.id + 1
        return next_id


    
    def get_actors(self) -> List[Actor]:
        return self._actors
   
    def get_genres(self) -> List[Genre]:
        return self._genres
  
    def get_directors(self) -> List[Director]:
        return self._directors
    
    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].year == movie.year:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_movies_and_tags(data_path: str, repo: MemoryRepository):
    #Rank,Title,Genre,Description,Director,Actors,Year,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore
    for row in read_csv_file(os.path.join(data_path, 'Data1000MoviesWithPics.csv')):
        movie = Movie(row[1], int(row[6]))
        movie.description = row[3]
        # genres
        genre_list = row[2].split(",")
        for genre in genre_list:
            movie.add_genre(Genre(genre.strip()))

        # director
        movie.add_director(Director(row[4]))

        # actors
        actors_list = row[5].split(",")
        for actor in actors_list:
            movie.add_actor(Actor(actor.strip()))

        movie.add_id(int(row[0]))
        path = "adapters/data/movie_posters_static/" + row[0] + ".jpg"
        movie.add_imagelink(row[12])

        # Add the movie to the repository.
        repo.add_movie(movie)




def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies_and_tags(data_path, repo)

