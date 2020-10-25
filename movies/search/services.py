from movies.adapters.repository import AbstractRepository
from movies.domain.allCombined import make_review, Movie, Review, Actor, Director, Genre

def search_exists(search, select, repo: AbstractRepository):


    if select == "Genre":
        if Genre(search) in repo.get_genres():
            return True
        else:
            return False

    elif select == "Director":
        if Director(search) in repo.get_directors():
            return True
        else:
            return False

    elif select == "Actor":
        if Actor(search) in repo.get_actors():
            return True
        else:
            return False

