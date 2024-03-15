import psycopg2 as pg
from datetime import datetime
from dotenv import load_dotenv
import os
import uuid
load_dotenv()


class DatabaseConnection:
    CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies(
        id SERIAL PRIMARY KEY,
        title TEXT,
        release_timestamp REAL
    );
    """
    CREATE_WATCHED_MOVIES_TABLE = "CREATE TABLE IF NOT EXISTS watched_movies(username TEXT, movie_id INTEGER);"

    CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users(ID uuid DEFAULT gen_random_uuid(), username TEXT PRIMARY KEY);"

    INSERT_USER = "INSERT INTO users(username) VALUES (%s);"
    SELECT_USER = "SELECT * FROM users WHERE username = %s;"
    INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"


    SELECT_ALL_MOVIES = "SELECT * FROM movies;"
    SELECT_MOVIES = "SELECT id, title FROM movies WHERE id = %s;"
    SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
    INSERT_WATCHED_MOVIE = "INSERT INTO watched_movies (username, movie_id) VALUES (%s, %s);"
    SELECT_WATCHED_MOVIES = """SELECT movies.*
    FROM users
    JOIN watched_movies ON users.username = watched_movies.user_username
    JOIN movies ON watched_movies.movie_id = movie_id
    WHERE users.username = %s;
    """
    SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE %S;"       
    CONNECTION = pg.connect(host=os.environ["DATABASE_HOST"], database=os.environ["DATABASE_NAME"], user=os.environ["DATABASE_USER"], password=os.environ["DATABASE_PASSWORD"])
    
    # def create_user(self, username):
    #     print(f"USERNAME TYPE {username}")
    #     with self.CONNECTION:
    #         with self.CONNECTION.cursor() as cursor:
    #             cursor.execute(self.CREATE_USERS_TABLE)
    #             cursor.execute(self.SELECT_USER, (username))
    #             res = cursor.fetchall()
    #             print(cursor)
    def add_movie(self, title, release_timestamp):
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(self.INSERT_MOVIE, (title, release_timestamp))

    def add_watched_movie(self, username, movie_id):
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(self.INSERT_WATCHED_MOVIE, (username, movie_id))

    def get_movie_list(self, movie_id):
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(self.SELECT_MOVIES, (movie_id))
                return cursor.fetchall()
            
    def get_movie(self, upcoming=False):
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                if upcoming:
                    today_timestamp = datetime.today().timestamp()
                    cursor.execute(self.SELECT_UPCOMING_MOVIES, (today_timestamp))
                else:
                    cursor.execute(self.SELECT_ALL_MOVIES)
                return cursor.fetchall()

    def add_user(self, username):
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                print(f"This is UUID : {uuid.uuid4()}")
                cursor.execute(self.INSERT_USER, (username, ))
                if(cursor.rowcount == 1):
                    return True
                else:
                    return False


    def watch_movie(self, username, movie_id):
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(self.INSERT_WATCHED_MOVIE, (username, movie_id))
                return cursor.rowcount

    def get_watched_movies(self, username):
        with self.CONNECTION:
            cursor = self.CONNECTION.cursor()
            cursor.execute(self.SELECT_WATCHED_MOVIES, (username))
            return cursor.fetchall()

    def serach_movies(self, search_item):
        with self.CONNECTION:
            cursor = self.CONNECTION.cursor()
            cursor.execute(self.SEARCH_MOVIE, (f"%{search_item}%"))
            return cursor.fetchall()
    
    def get_user(self, username):
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(self.SELECT_USER, (username,))
                results = cursor.fetchall()
                return results
        
    def create_tables(self, query):
        if(query == "users"):
            execute_query = self.CREATE_USERS_TABLE
        elif(query == "movies"):
            execute_query = self.CREATE_MOVIES_TABLE
        elif(query == "watched_movies"):
            execute_query = self.CREATE_WATCHED_MOVIES_TABLE
        print(execute_query)
        with self.CONNECTION:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(execute_query)

if __name__ == '__main__':
    connectionObject = DatabaseConnection()