#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print()
import mysql.connector as mysqlconn

# CREATE CONNECTION
conn = mysqlconn.connect(host="localhost", user="root", password="")

# CREATE A CURSOR
mycursor = conn.cursor()

# USE THE DATABASE CALLED "discourse"
mycursor.execute("USE discourse")
