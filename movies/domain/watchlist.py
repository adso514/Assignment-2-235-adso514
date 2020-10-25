from domain.movie import Movie

class WatchList:
    def __init__(self):
        self.__watch_list = []
        
    def __iter__(self):
        self.i = -1
        return self
        
    def __repr__(self):
        return repr(self.__watch_list)
    
     def __next__(self):
        if self.i < len(self.__watch_list) -1:
            self.i += 1
            result = self.__watch_list[self.i]
            
            return result
        else:
            raise StopIteration
            
    def add_movie(self, movie: Movie):
        if movie not in self.__watch_list and type(movie) is Movie:
            self.__watch_list.append(movie)
            
            
    def remove_movie(self, movie: Movie):
        if movie in self.__watch_list and type(movie) is Movie :
            self.__watch_list.remove(movie)
                    
                    
    def select_movie_to_watch(self, index: int):
        if index >= 0 and index < len(self.__watch_list):
            return self.__watch_list[index]
        else:
            return None
            
            
    def size(self):
        return len(self.__watch_list)
        
        
    def first_movie_in_watchlist(self):
        if len(self.__watch_list) > 0:
            return self.__watch_list[0]
        else:
            return None
            


    


   