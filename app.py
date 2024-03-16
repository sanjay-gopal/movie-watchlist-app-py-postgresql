from database import DatabaseConnection as db
from datetime import datetime

class MoviesWatchlist():
    welcome_message = "Welcome to the watchlist app! Press enter key"
    menu = """Please select one of the following options:
    1) Add new movie.
    2) View upcoming movies.
    3) View all movies
    4) Watch a movie
    5) View watched movies.
    6) Exit.

    Your selection: """

    CURRENT_USER = ""
    def add_movie(self, title, release_date):
        release_timestamp = datetime.today().strptime(release_date, "%d-%m-%Y").timestamp()
        try:
            res = db.add_movie(db, title, release_timestamp)
            return res
        except Exception as exp:
            return exp
    
    def get_upcoming_movies(self, upcoming):
        results = db.get_movie(db, upcoming)
        self.show_formatted_movies_list(results)

    def get_movies(self):
        results = db.get_movie(db)
        self.show_formatted_movies_list(results)
    
    def show_formatted_movies_list(self, results):
        print("S.No     Movie Name     Release Date")
        print("_____________________________________")
        print("S.No  |   Movie Name  |  Release Date")
        print("_____________________________________")
        for i,j,k in results:
            print("{:<14}{:<11}{}".format(i, j, datetime.fromtimestamp(k).date()))
            print("--------------------------------------")

    def verify_user(self, username):
        db.create_tables(db, query="users")
        users_list = db.get_user(db, username)
        if len(users_list) > 0 and username in users_list[0]:
            self.CURRENT_USER = username

            return True
        else:
            return False
    
    def check_movie_available(self, movie_id):
        res = db.get_movie_list(db, movie_id)
        if(res != []):
            print(f"Movie {res[0][1]} Found. Press enter to watch it! ")
            return True
        else:
            print("Movie with ID {movie_id} was not found!")
            return False
    
    # def view_watched_movies(self):
    #     results = db.get_watched_movies(db, self.CURRENT_USER)
    #     self.show_formatted_movies_list(results)

    def show_menu(self):
        while (user_input := input(movieObject.menu)) != "6":
            if user_input == "1":
                title = str(input("Movie title : "))
                release_date =  input("Release date (mm-dd-YYYY): ") or datetime.today().strftime("%d-%m-%Y")
                movieObject.add_movie(title, release_date)

            elif user_input == "2":
                upcoming = str(input("Do you also want to see upcoming movies list? (Y/N): ").upper())
                if upcoming == "Y": 
                    upcoming = True
                else: 
                    upcoming = False
                movieObject.get_upcoming_movies(upcoming)

            elif user_input == "3":
                movieObject.get_movies()

            elif user_input == "4":
                results = db.get_movie(db)
                movieObject.show_formatted_movies_list(results)
                movie_id = input("Enter the movie ID to watch: ")
                res = movieObject.check_movie_available(movie_id)
                if(res):
                    db.watch_movie(db, "", movie_id)
                    print("Watching Movie...........")
                    exit(1)
                else:
                    exit(1)

            elif user_input == "5":
                results = db.get_watched_movies(db, self.CURRENT_USER)
                movieObject.show_formatted_movies_list(results)
            else:
                print("Invalid input, please try again!")

if __name__ == "__main__":
    movieObject = MoviesWatchlist()
    username = input("To begin, please choose a username. Enter your desired username and press the Enter key to proceed : ")
    movieObject.CURRENT_USER = username
    verified_user = movieObject.verify_user(username)
    if(verified_user):
        movieObject.show_menu()
    else:
        username = input("User not found. Please enter a username to create a new user profile : ")
        user_created = db.add_user(db, username)
        if(user_created):
            db.create_tables(db, query="movies")
            db.create_tables(db, query="watched_movies")
            movieObject.show_menu()
        else:
            print("Oops! Something went wrong. Please try again later.")
