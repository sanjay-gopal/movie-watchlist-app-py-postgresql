import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()


class DatabaseConnection:
    CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies(
        id SERIAL PRIMARY KEY,
        title TEXT,
        release_timestamp REAL
    );
    """

    CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
    );
    """

    INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
    SELECT_ALL_MOVIES = "SELECT * FROM movies;"
    SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
    INSERT_USER = "INSERT INTO users(username) VALUES (%S)"
    INSERT_WATCHED_MOVIE = "INSERT INTO watched (username, movie_id) VALUES (%S, %S);"
    SELECT_WATCHED_MOVIES = """SELECT movies.*
    FROM users
    JOIN watched ON users.username = watched.user_username
    JOIN movies ON watched.movie_id = movie_id
    WHERE users.username = %s;
    """
    SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE %S;"       

    def __init__(self, connection):
        self.connection = connection

    def add_movie(self, title, release_timestamp):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(self.INSERT_MOVIE, (title, release_timestamp))


    def get_movie(self, upcoming=False):
        with self.connection:
            with self.connection.cursor() as cursor:
                if upcoming:
                    today_timestamp = datetime.datetime.today().timestamp()
                    cursor.execute(self.SELECT_UPCOMING_MOVIES, (today_timestamp))
                else:
                    cursor.execute(self.SELECT_ALL_MOVIES)
                return cursor.fetchall()

    def add_user(self, username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(self.INSERT_USER, (username))


    def watch_movie(self, username, movie_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(self.INSERT_WATCHED_MOVIE, (username, movie_id))

    def get_watched_movies(self, username):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.SELECT_WATCHED_MOVIES, (username))
            return cursor.fetchall()

    def serach_movies(self, search_item):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.SEARCH_MOVIE, (f"%{search_item}%"))
            return cursor.fetchall()

    def create_movies_table(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.CREATE_MOVIES_TABLE)
            return cursor


connection = psycopg2.connect(host=os.environ["DATABASE_HOST"], database=os.environ["DATABASE_NAME"], user=os.environ["DATABASE_USER"], password=os.environ["DATABASE_PASSWORD"])
connectionObject = DatabaseConnection(connection)