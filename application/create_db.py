import sqlite3

connection = sqlite3.connect("trinity.db")
cursor = connection.cursor()
# путь до скрипта с инструкциями по созданию БД
with open("application/create_db.sql", "r") as f:
    command = f.read()
cursor.executescript(command)
cursor.close()
connection.close()
