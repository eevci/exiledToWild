import MySQLdb

db=MySQLdb.connect("localhost","root","grg170dx","ETW")
cursor=db.cursor()
query=""
query+="truncate table Animals;"
cursor.execute(query)
query=""
query+="truncate table Users;"
cursor.execute(query)
query=""
query+="truncate table Weapons;"
cursor.execute(query)
query=""
query+="truncate table Inventories;"
cursor.execute(query)
query=""
query+="truncate table Trees;"
cursor.execute(query)
db.commit()

db.close()