from database import DatabaseConnection as db
from datetime import datetime

class MoviesWatchlist():
    welcome_message = "Welcome to the watchlist app! \n Press enter key"
    menu = """Please select one of the following options:
    1) Add new movie.
    2) View upcoming movies.
    3) View all movies
    4) Watch a movie
    5) View watched movies.
    6) Exit.

    Your selection: """

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
            datetime.fromtimestamp(1710313200).date()
            print("{:<14}{:<11}{}".format(i, j, datetime.fromtimestamp(k).date()))
            print("--------------------------------------")

    def verify_user(self, username):
        db.create_tables(db, query="users")
        users_list = db.get_user(db, username)
        print(users_list)
        if len(users_list) > 0 and username in users_list[0]:
            return True
        else:
            return False
    
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
                pass
            elif user_input == "5":
                pass
            else:
                print("Invalid input, please try again!")

if __name__ == "__main__":
    movieObject = MoviesWatchlist()
    username = input("To begin, please choose a username. Enter your desired username and press the Enter key to proceed : ")
    verified_user = movieObject.verify_user(username)
    if(verified_user):
        print(movieObject.welcome_message)
        movieObject.show_menu()
    else:
        username = input("User not found. Please enter a username to create a new user profile : ")
        user_created = db.add_user(db, username)
        if(user_created):
            print(movieObject.welcome_message)
            movieObject.show_menu()
        else:
            print("Oops! Something went wrong. Please try again later.")
