import sqlite3 as sql

#connect to SQLite
con = sql.connect('carsweb.db')

#Create a Connection
cur = con.cursor()

#Drop users table if already exsist.
cur.execute("DROP TABLE IF EXISTS tbcars")

#Create users table  in db_web database
sql ='''CREATE TABLE "tbcars" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"carname"	TEXT NOT NULL,
    "carbrand"  TEXT NOT NULL,
	"carmodel"	TEXT NOT NULL,
    "carprice"  TEXT NOT NULL
)'''
cur.execute(sql)

#commit changes
con.commit()

#close the connection
con.close()