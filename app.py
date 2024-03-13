from database import connectionObject
from datetime import datetime
menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"

def add_movie():
    connectionObject.create_movies_table()
    title = str(input("Movie title : "))
    release_date =  input("Release date (mm-dd-YYYY): ") or datetime.today().strftime("%d-%m-%Y")
    release_timestamp = datetime.today().strptime(release_date, "%d-%m-%Y").timestamp()
    print(f"Title: {title}, Release Timestamp: {release_timestamp}")
    try:
        connectionObject.add_movie(title, release_timestamp)
    except Exception as e:
        return e

while (user_input := input(menu)) != "6":
    if user_input == "1":
        add_movie()
    elif user_input == "2":
        pass
    elif user_input == "3":
        pass
    elif user_input == "4":
        pass
    elif user_input == "5":
        pass
    else:
        print("Invalid input, please try again!")
