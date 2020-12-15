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
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

if x.connection is not None:
    x.create_table(sql_create_projects_table)
    x.create_table(sql_create_tasks_table)
else:
    print("Error! cannot create the database connection.")