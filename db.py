from sensinfo import *
import mysql.connector as mysql 

db = mysql.connect(
    host="localhost",
    user= DB_USERNAME,
    password= DB_PASSWORD,
    database= DB
)

cursor = db.cursor()

