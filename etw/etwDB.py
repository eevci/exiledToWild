import MySQLdb



def newAnimal(animal):
	
	
	query="INSERT INTO Animals (animalID,animalName,animalType,animalHealth,animalPositionX,"
	query+="animalPositionY,animalWaitingSec,animalAttPow) VALUES ("+str(animal.id)+",\"" +animal.name+"\"      "
	query+=","+ str(animal.type)+","+str(animal.health)+","+ str(animal.pos[0])+","+str(animal.pos[1])+","+str(animal.attacked)+","+str(animal.att_pow)+" );"
	
	return query
	
def updateAnimal(animal):
	
	
	query="Update Animals set animalHealth="+str(animal.health)+" , animalPositionX="+str(animal.pos[0])+",animalPositionY="+str(animal.pos[1])+" where animalID="+str(animal.id)+";"
	return query
	
def delAnimal(animal):

	query="Delete from Animals where animalID="+str(animal.id)+";"
	return query
	


def newWeapon(weapon):
	
	
	query="INSERT INTO Weapons (weaponID,weaponName,weaponType,weaponHealth,weaponPositionX,"
	query+="weaponPositionY,weaponAttPow,weaponHReduction) VALUES ("+str(weapon.id)+",\"" +weapon.name+"\""
	query+=","+ str(weapon.type)+","+str(weapon.health)+","+ str(weapon.pos[0])+","+str(weapon.pos[1])+","+str(weapon.att_pow)+","+str(weapon.healthreduction)+" );"
	
	return query
	
def updateWeapon(weapon):
	
	
	query="Update Weapons set weaponHealth="+str(weapon.health)+" , weaponPositionX="+str(weapon.pos[0])+",weaponPositionY="+str(weapon.pos[1])+" where weaponID="+str(weapon.id)+";"
	return query
	
def delWeapon(weapon):
	
	
	query="Delete from Weapons where weaponID="+str(weapon.id)+";"
	return query
	


def newUser(user):
	
	
	query="INSERT INTO Users (userID,userName,userType,userHealth,userPositionX,"
	query+="userPositionY,userHoldingID,userExp,userLvl,userColor,userDirection,userInvID,userOnline) VALUES ("+str(user.id)+",\"" +user.username+"\"      "
	query+=","+ str(user.type)+","+str(user.health)+","+ str(user.pos[0])+","+str(user.pos[1])+","+str(user.holding.id)
	query+=","+str(user.exp)+","+str(user.lvl)+",\""+str(user.color)+"\",\""+str(user.direction)+"\" ,"+str(user.id)+","+str(user.online)+" );" 
	return query
	
def updateUser(user):
	
	query="Update Users set userHealth="+str(user.health)+" , userPositionX="
	query+=str(user.pos[0])+",userPositionY="+str(user.pos[1])+",userHoldingID="+str(user.holding.id)+" ,userLvl="+str(user.lvl)+",userOnline="+str(user.online) 
	query+=",userExp="+str(user.exp)+",userDirection=\""+str(user.direction)+"\" where userID="+str(user.id)+";"
	print query
	return query
	
def delUser(user):
	
	query="Delete from Users where userID="+str(user.id)+";"
	return query
	
	




def newInv(user,weapon):
	
	query="INSERT INTO Inventories (invID,weaponID) VALUES ("+str(user.id)+", " +str(weapon.id)+");"
	return query
	
def delInv(user,weapon):
	
	query="Delete from Inventories where invID="+str(user.id)+" and weaponID="+str(weapon.id)+";"
	return query
	



def newTree(tree):
	
	query="INSERT INTO Trees (treeID,treeType,treeHealth,treePosX,treePosY) VALUES ("+str(tree.id)+", " +str(tree.type)
	query+=","+str(tree.health)+","+str(tree.pos[0])+","+str(tree.pos[1])+");"
	return query
	
def updateTree(tree):
	
	query="Update Trees set treeHealth="+str(tree.health)+" where treeID="+str(tree.id)+";"
	return query
	
def delTree(tree):
	
	query="Delete from Trees where treeID="+str(tree.id)+";"
	return query

'''
@Singleton
class Query:
	def __init__(self):
		self.query=[]
		self.mysqlUname="root"
		self.password="1111"
		self.dbname="ETW"
	def addQuery(self,q):
		self.query.append(q)

	def executeQuery(self):
		db=MySQLdb.connect("localhost",self.mysqlUname,self.password,self.dbname)
		cursor=db.cursor()
		for i in self.query:
			if i:
				cursor.execute(i)
				db.commit()
		db.close()		
			
	def emptyQuery(self):
		self.query=[]
	def closeConn(self):
		self.db.close()
		print "Connection Closed.."



db=MySQLdb.connect("localhost","root","grg170dx","ETW")
cursor=db.cursor()
query=""
query+=("create table Trees(")
query+=("treeID INT NOT NULL PRIMARY KEY,")
query+=("treeType INT NOT NULL ,")
query+=("treeHealth INT NOT NULL ,")
query+=("treePosX INT NOT NULL ,")
query+=("treePosY INT NOT NULL );")
cursor.execute(query)
data=cursor.fetchone()

db.close()

db=MySQLdb.connect("localhost","root","grg170dx","ETW")
cursor=db.cursor()
query=""
query+=("create table Inventories(")
query+=("invID INT NOT NULL ,")
query+=("weaponID INT NOT NULL );")
cursor.execute(query)
data=cursor.fetchone()

db.close()
db=MySQLdb.connect("localhost","root","grg170dx","ETW")
cursor=db.cursor()
query=""
query+=("create table Weapons(")
query+=("weaponID INT NOT NULL PRIMARY KEY,")
query+=("weaponName varchar(10) not null,")
query+=("weaponType int not null,")
query+=("weaponHealth int not null,")
query+=("weaponPositionX int not null,")
query+=("weaponPositionY int not null,")
query+=("weaponAttPow int not null,")
query+=("weaponHReduction int not null);")
cursor.execute(query)

db.close()

db=MySQLdb.connect("localhost","root","grg170dx","ETW")
cursor=db.cursor()
query=""
query+=("create table Users(")
query+=("userID INT NOT NULL PRIMARY KEY,")
query+=("userName varchar(10) not null,")
query+=("userType int not null,")
query+=("userHealth int not null,")
query+=("userPositionX int not null,")
query+=("userPositionY int not null,")
query+=("userHoldingID int not null,")
query+=("userExp int not null,")
query+=("userLvl int not null,")

query+=("userColor varchar(10) not null,")
query+=("userDirection varchar(10) not null,")
query+=("userInvID int not null),
query+=("userOnline int not null);")  ********************************************************************
cursor.execute(query)


db.close()

db=MySQLdb.connect("localhost","root","grg170dx","ETW")
cursor=db.cursor()
query=""
query+=("create table Animals(")
query+=("animalID INT NOT NULL PRIMARY KEY ,")
query+=("animalName varchar(10) not null,")
query+=("animalType int not null,")
query+=("animalHealth int not null,")
query+=("animalPositionX int not null,")
query+=("animalPositionY int not null,")
query+=("animalWaitingSec int not null,")
query+=("animalAttPow int not null);")
cursor.execute(query)


db.close()

'''