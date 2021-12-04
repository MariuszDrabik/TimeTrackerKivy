import sqlite3
from sqlite3 import Error


class ConnectSQLite:

    @staticmethod
    def create_connection():
        db_file = 'database/time.db'
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            return conn

    def drop_table(self, table):
        with self.create_connection() as c:
            cursor = c.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS {table}')


class TrackRepository:

    def __init__(self):
        self.conn = ConnectSQLite.create_connection()

    def get_by_id(self, project_id):
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute(''' SELECT Projects.name, project_time FROM Tracks
                           LEFT JOIN Projects ON Projects.id = project_ID WHERE
                           Projects.id=?''', (project_id,))
            return cursor.fetchall()

    def get_all(self):
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT Projects.name, start_time, end_time,
                           project_time FROM Tracks LEFT JOIN Projects ON
                           Projects.id = project_ID''')
            return cursor.fetchall()

    def save(self, project_id, start_time, end_time, project_time):
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO Tracks ('
                '`project_ID`, `start_time`, `end_time`, `project_time`)'
                'VALUES(?, ?, ?, ?)',
                (project_id, start_time, end_time, project_time))
            connection.commit()


class ProjectRepository:

    def __init__(self):
        self.conn = ConnectSQLite().create_connection()

    def get_all(self):
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT `id`,`name` FROM Projects')
            return cursor.fetchall()

    def get_id(self, name):
        with self.conn as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT `id` FROM Projects WHERE name=?', (name,))
            return cursor.fetchone()

    def save(self, name):
        with self.conn as connection:
            cursor = connection.cursor()
            if self.get_id(name):
                print("Projekt istniej wybierz inna nazwę")
                return False
            cursor.execute("INSERT INTO Projects (`name`) VALUES(?)", (name,))
            connection.commit()


if __name__ == '__main__':
    pass
