import json
import sqlite3
from NetworkService import UNOGSRequestProtocol as request
import os


class DatabaseHelper:
    @staticmethod
    def open_json_file():
        request_network_service = request()
        response_network_service = request_network_service.get_data()
        with open(response_network_service, 'r') as file:
            return json.load(file)

    @staticmethod
    def connect_to_database():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'MovieDatabaseApp-2.0.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                    _id TEXT,
                    overview TEXT,
                    genres TEXT,
                    poster_path TEXT,
                    title TEXT,
                    release_date TEXT
                )''')

        return conn, cursor

    @staticmethod
    def write_to_database(data, conn, cursor):
        for item in data:
            _id = item.get('_id')
            overview = item.get('overview')
            genres = ', '.join(item.get('genres', []))
            poster_path = item.get('poster_path')
            title = item.get('title')
            release_date = item.get('release_date')

            cursor.execute('''INSERT INTO movies (_id, overview, genres, poster_path, title, release_date)
                              VALUES (?, ?, ?, ?, ?, ?)''', (_id, overview, genres, poster_path, title, release_date))

        # Сохраняем изменения в базе данных и закрываем соединение
        conn.commit()
        conn.close()