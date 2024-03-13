from database import DatabaseConnection as db
from datetime import datetime

class MoviesWatchlist():
    menu = """Please select one of the following options:
    1) Add new movie.
    2) View upcoming movies.
    3) View all movies
    4) Watch a movie
    5) View watched movies.
    6) Exit.

    Your selection: """
    welcome = "Welcome to the watchlist app!"

    def add_movie(self):
        title = str(input("Movie title : "))
        release_date =  input("Release date (mm-dd-YYYY): ") or datetime.today().strftime("%d-%m-%Y")
        release_timestamp = datetime.today().strptime(release_date, "%d-%m-%Y").timestamp()
        try:
            res = db.add_movie(db, title, release_timestamp)
            return res
        except Exception as exp:
            return exp
    
    def get_upcoming_movies(self):
        upcoming = str(input("Do you also want to see upcoming movies list? (Y/N): ").upper())
        if upcoming == "Y": 
            upcoming = True
        else: 
            upcoming = False
        results = db.get_movie(db, upcoming)
        print("S.No     Movie Name     Release Date")
        print("_____________________________________")
        print("S.No  |   Movie Name  |  Release Date")
        print("_____________________________________")
        for i,j,k in results:
            datetime.fromtimestamp(1710313200).date()
            print("{:<14}{:<11}{}".format(i, j, datetime.fromtimestamp(k).date()))
            print("--------------------------------------")


if __name__ == "__main__":
    movieObject = MoviesWatchlist()
    while (user_input := input(movieObject.menu)) != "6":
        if user_input == "1":
            movieObject.add_movie()
        elif user_input == "2":
            movieObject.get_upcoming_movies()
        elif user_input == "3":
            pass
        elif user_input == "4":
            pass
        elif user_input == "5":
            pass
        else:
            print("Invalid input, please try again!")