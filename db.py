import sqlite3

db = sqlite3.connect("db.sqlite3", check_same_thread=False )
cursor = db.cursor()