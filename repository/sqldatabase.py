import sqlite3


class SQLDataBase:
    def __init__(self, file_path=r'my_data_base.db'):
        self.database_file = file_path
        self.connection = None

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.database_file)
        except Exception as e:
            raise e
        finally:
            if self.connection:
                # self.connection.close()
                pass

    def create_table(self, SQL_statement):
        try:
            cursor = self.connection.cursor()
            cursor.execute(SQL_statement)
        except Exception as e:
            print(e)


x = SQLDataBase('mydatabase')
x.create_connection()

book_table = '''CREATE TABLE BOOK
         (ID INT PRIMARY KEY     NOT NULL,
         TITLE           TEXT    NOT NULL,
         AUTHOR            TEXT     NOT NULL);'''

client_table = '''CREATE TABLE CLIENT
         (ID INT PRIMARY KEY     NOT NULL,
         NAME          TEXT    NOT NULL);'''

client_table = '''CREATE TABLE RENTAL
         (ID INT PRIMARY KEY     NOT NULL,
         BOOK_ID           INT    NOT NULL,
         CLIENT_ID            INT     NOT NULL,
         RENTED_DATE            TEXT     NOT NULL,
         RETURNED_DATE            TEXT     NOT NULL);'''


if x.connection is not None:
    x.create_table(book_table)
    x.create_table(client_table)
else:
    print("Error! cannot create the database connection.")