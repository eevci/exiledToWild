import random
import re
import os
import itertools
from threading import *
from etwLists import *
from etwDB import *

host="localhost"
databaseName="ETW"
usr="root"
password="grg170dx"


#Exiled To Wild
#Authors: Enver Evci, Onat Buyukakkus
_id = itertools.count()
def Singleton(cls):
	'''generic python decorator to make any class
	singleton.'''
	_instances = {}	  # keep classname vs. instance
	def getinstance():
		'''if cls is not in _instances create it
		and store. return the stored instance'''
		if cls not in _instances:
			_instances[cls] = cls()
		return _instances[cls]
	return getinstance

@Singleton
class Query:
	def __init__(self):
		self.query=[]
		
	def addQuery(self,q):
		self.query.append(q)

	def executeQuery(self):
		
		db=MySQLdb.connect(host,usr,password,databaseName)
		cursor=db.cursor()
		for i in self.query:
			if i:
				
				cursor.execute(i)
				db.commit()
		db.close()		
		self.emptyQuery()	
	def emptyQuery(self):
		self.query=[]

def getID():
		i=next(_id)
		return i


class Item(object):
	_ID=0
	def __init__(self):
		self._id = self._ID 
		self.__class__._ID += 1

class User(Item):
	
	def __init__(self,username,x,y,id):
		self.id=id
		self.username=username
		self.health=100
		self.type=5
		self.pos=[x,y]	
		self.inventory=[Weapon(self.pos[0],self.pos[1],"Punch",-1)]
		self.holding=self.inventory[0]
		self.exp=0
		self.lvl=1
		self.color="black"
		self.direction=directions[0]
		self.online=1; 

	def __repr__(self):
		return  self.username

	def printInv(self):
		pinv=["["]
		for i in self.inventory:
			if i.name!="Punch":
				pinv.append(repr(i))
				pinv.append(",")
		if len(pinv)!=1:
			del pinv[-1]
		
		pinv.append("]")
		return ''.join(pinv)
	
	def user_Map(self):
		myMap=Grid()
		message=[]
		n=5
		for i in range(self.pos[0]-5,self.pos[0]+6):
			row=[]
			for t in range(self.pos[1]-5,self.pos[1]+6):
				try:
					row.append(repr(myMap.pixels[i][t]))
				except:
					continue
			message.append(row)

		return message
		

	def userCutTree(self,lock):
		myMap=Grid()
		query=Query()
		message=[]
		lock.acquire()
		if(self.direction==directions[0]):	
			temp=myMap.pixels[self.pos[0]-1][self.pos[1]]
			
		elif(self.direction==directions[1]):	
			temp=myMap.pixels[self.pos[0]+1][self.pos[1]]
				
		elif(self.direction==directions[2]):	
			temp=myMap.pixels[self.pos[0]][self.pos[1]+1]
					
		elif(self.direction==directions[3]):	
			temp=myMap.pixels[self.pos[0]][self.pos[1]-1]

		if(temp.type==2):
			message.append("You hit the tree with: "+str(self.holding.att_pow)+" attack power\n")
			
			temp.health-=self.holding.att_pow+self.lvl
			query.addQuery(updateTree(temp))
			if(temp.health<=0):
				message.append("You have cut the tree!")
				query.addQuery(delTree(temp))
				myMap.pixels[temp.pos[0]][temp.pos[1]]=Grass()
			
			if(self.holding.name!="Punch"):
				self.holding.health-=5
				query.addQuery(updateWeapon(self.holding))
			if(self.holding.health<=0):
				message.append("Your weapon is broken")
				print "=="
				query.addQuery(delWeapon(self.holding))
				print "delweapon bitti"
				query.addQuery(delInv(self,self.holding))
				print "delinv bitti"
				
				
				self.holding = self.inventory[0]
				print "holding bitti"
				query.addQuery(updateUser(self))
		lock.release()
		return message

	def userAttack(self,lock):
		myMap=Grid()
		query=Query()
		message=[]
		lock.acquire()
		try:
			if(self.direction==directions[0]):		
				temp=myMap.pixels[self.pos[0]-1][self.pos[1]]
				
			elif(self.direction==directions[1]):	
				temp=myMap.pixels[self.pos[0]+1][self.pos[1]]
					
			elif(self.direction==directions[2]):	
				temp=myMap.pixels[self.pos[0]][self.pos[1]+1]
						
			elif(self.direction==directions[3]):	
				temp=myMap.pixels[self.pos[0]][self.pos[1]-1]
				
			
			if(temp.type in attackTypeList):
				print "lock ustu"
				
				print "lock alti"
				if(temp.type==5):
					
					temp.health-=self.holding.att_pow+self.lvl*5
					
					query.addQuery(updateUser(temp))
					message.append(str(self.holding.att_pow+self.lvl*5)+" Hit \n")
					self.holding.health-=self.holding.healthreduction
					query.addQuery(updateWeapon(self.holding))
					

				
				elif(temp.type==3):
					
					temp.health-=self.holding.att_pow+self.lvl*5
					temp.attacked=10

					query.addQuery(updateAnimal(temp))
					message.append(str(self.holding.att_pow+self.lvl*5)+" Hit \n")
					self.holding.health-=self.holding.healthreduction
					query.addQuery(updateWeapon(self.holding))
					
					self.health-=animalList[temp.name]
					
					message.append(str(animalList[temp.name])+" damaged\n")
					
				
				if(self.holding.health<=0):
					
					
					message.append("Your weapon is broken")
					print "=="
					query.addQuery(delWeapon(self.holding))
					print "delweapon bitti"
					query.addQuery(delInv(self,self.holding))
					print "delinv bitti"
					
					
					self.holding = self.inventory[0]
					print "holding bitti"
					query.addQuery(updateUser(self))
	
				if(temp.health<=0):
					
					if(temp.type==5):
						self.exp+=10
						message.append(str(10)+" experience point gained\n")
						tmp=self.health
						self.health+=50
						if(self.health>100):
							self.health = 100
						message.append(str(50)+" health point restored\n")
					elif(temp.type==3):	
						print "ALALALA"
						myMap.pixels[temp.pos[0]][temp.pos[1]]=Grass()
						query.addQuery(delAnimal(temp))
						self.exp+=animalExpList[temp.name]
						message.append(str(animalExpList[temp.name])+" experience point gained\n")
						self.health+=animalList[temp.name]*5
						if(self.health>100):
							self.health = 100
						message.append(str(animalList[temp.name]*5)+" health point restored\n")
					if(lvlUpgrade[str(self.lvl+1)]<=self.exp):
						self.lvl+=1
						
						message.append("Level Up!\n")

				query.addQuery(updateUser(self))
				query.executeQuery()
				lock.release()
				if temp.type==5:
					return [message,temp]	
				return [message]
		except:
			lock.release()
		lock.release()
		return [["You couldn't attack"]]
	def addToInventory(self,lock):
		myMap=Grid()
		query=Query()
		message=[]
		lock.acquire()
		if(self.direction==directions[0]):		
			temp=myMap.pixels[self.pos[0]-1][self.pos[1]]
			
		elif(self.direction==directions[1]):	
			temp=myMap.pixels[self.pos[0]+1][self.pos[1]]
				
		elif(self.direction==directions[2]):	
			temp=myMap.pixels[self.pos[0]][self.pos[1]+1]
				
		elif(self.direction==directions[3]):	
			temp=myMap.pixels[self.pos[0]][self.pos[1]-1]

		if(temp.type==4):
			index=None
			for i in range(1,len(self.inventory)):
				if self.inventory[i].name==temp.name:
					index=i

			if index:
				x=temp.pos[0]
				y=temp.pos[1]
				myMap.pixels[temp.pos[0]][temp.pos[1]]=self.inventory[index]
				temp.pos[0]=self.pos[0]
				temp.pos[1]=self.pos[1]
				self.inventory[index].pos[0]=x
				self.inventory[index].pos[1]=y
				print "temp pos= "+str(temp.pos[0])+" "+str(temp.pos[1])
				print "self.inventory pos= "+str(self.inventory[index].pos[0])+" "+str(self.inventory[index].pos[1])
				query.addQuery(updateWeapon(temp))
				query.addQuery(updateWeapon(self.inventory[index]))
				query.addQuery(delInv(self,self.inventory[index]))

				self.inventory[index]=temp
				query.addQuery(newInv(self,temp))

				self.holding=self.inventory[0]
				query.addQuery(updateUser(self))
				message.append(temp.name+" is changed with the old one")

			else:
				myMap.pixels[temp.pos[0]][temp.pos[1]]=Grass()
				self.inventory.append(temp)

				query.addQuery(newInv(self,temp))
				message.append(temp.name+ " is added to inventory")
		lock.release()
		return message

	def selectInventory(self,name):
		query=Query()
		message=[]
		for i in self.inventory:
			if (i.name==name):
				self.holding=i
				
				message.append("Now, you are holding "+name)
				query.addQuery(updateUser(self))
				return message
		message.append("You don't have "+name+" in your inventory!")
		query.addQuery(updateUser(self))
		return message

	def userMove(self,lock):
		myMap=Grid()
		query=Query()
		message=[]
		lock.acquire()
		if(self.direction=="Up"):
			try:
				if(myMap.pixels[self.pos[0]-1][self.pos[1]].type==1):
					
					myMap.pixels[self.pos[0]-1][self.pos[1]]=self
					myMap.pixels[self.pos[0]][self.pos[1]]=Grass()
					self.pos[0]=self.pos[0]-1
					for i in self.inventory:
						i.pos[0]=self.pos[0]
						i.pos[1]=self.pos[1]
					
				else:
					message.append("Can't move that way")
			except:
				message.append("Can't move that way")

		elif(self.direction=="Down"):
			try:
				if(myMap.pixels[self.pos[0]+1][self.pos[1]].type==1):
					
					myMap.pixels[self.pos[0]+1][self.pos[1]]=self
					myMap.pixels[self.pos[0]][self.pos[1]]=Grass()
					self.pos[0]+=1
					for i in self.inventory:
						i.pos[0]=self.pos[0]
						i.pos[1]=self.pos[1]
					
				else:
					message.append("Can't move that way")
			except:
				message.append("Can't move that way")

		elif(self.direction=="Right"):
			try:
				if(myMap.pixels[self.pos[0]][self.pos[1]+1].type==1):
					
					myMap.pixels[self.pos[0]][self.pos[1]+1]=self
					myMap.pixels[self.pos[0]][self.pos[1]]=Grass()
					
					self.pos[1]+=1
					for i in self.inventory:
						i.pos[0]=self.pos[0]
						i.pos[1]=self.pos[1]
				else:
					message.append("Can't move that way")
			except:
				message.append("Can't move that way")

		elif(self.direction=="Left"):
			try:
				if(myMap.pixels[self.pos[0]][self.pos[1]-1].type==1):
					
					myMap.pixels[self.pos[0]][self.pos[1]-1]=self
					myMap.pixels[self.pos[0]][self.pos[1]]=Grass()
					
					self.pos[1]=self.pos[1]-1
					for i in self.inventory:
						i.pos[0]=self.pos[0]
						i.pos[1]=self.pos[1]
				else:
					message.append("Can't move that way")
			except:
				message.append("Can't move that way")

		for i in self.inventory:
			query.addQuery(updateWeapon(i))
		query.addQuery(updateUser(self))
		lock.release()
		return message

	def userChangeDirection(self,direction):
		if direction in directions:
			query=Query()
			self.direction=direction
			query.addQuery(updateUser(self))

	def sleep(self):
		query=Query()
		self.health+=25
		if(self.health>100):
			self.health = 100
		query.addQuery(updateUser(self))

class Lake(Item):

	def __init__(self):
		self.name="~"
		self.type=0
		
	def __repr__(self):
		return self.name

class Grass(Item):

	def __init__(self):
		self.name="."
		self.type=1	

	def __repr__(self):
		return self.name

class Tree(Item):
	
	def __init__(self,id):
		self.name="|"
		self.type=2
		self.health=50
		self.pos=[0,0]
		self.id=id

	def __repr__(self):
		return self.name + "(" + str(self.health)+ ")"

class Animal(Item):
	
	def __init__(self,x,y,att_pow,name,id):	
		self.type=3
		self.id=id
		self.health=100
		self.att_pow=att_pow
		self.pos=[x,y]
		self.name=name
		self.attacked=0

	def __repr__(self):
		return self.name + "(" + str(self.health)+ ")" 
	
	def stuck(self):
		myMap=Grid()
		__stuck=True
		try:
			if(myMap.pixels[self.pos[0]+1][self.pos[1]].type==1):
				__stuck=False
		except:
			pass
		try:
			if(myMap.pixels[self.pos[0]-1][self.pos[1]].type==1):
				__stuck=False
		except:
			pass
		try:
			if(myMap.pixels[self.pos[0]][self.pos[1]+1].type==1):
				__stuck=False
		except:
			pass
		try:
			if(myMap.pixels[self.pos[0]][self.pos[1]-1].type==1):
				__stuck=False
		except:
			pass

		return __stuck

	def animalMove(self):
		myMap=Grid()
		
		query=Query()
		if(self.stuck()!=True and self.attacked==0):
			
			while(True):
				x=random.randint(-1,1)
				y=random.randint(-1,1)
				
				try:
					
					if(myMap.pixels[self.pos[0]+x][self.pos[1]+y].type==1):
						myMap.pixels[self.pos[0]][self.pos[1]]=Grass()
						myMap.pixels[self.pos[0]+x][self.pos[1]+y]=self
						self.pos=[self.pos[0]+x,self.pos[1]+y]
						query.addQuery(updateAnimal(self))
						break
				except:

					x,y=0,0
					continue

class Weapon(Item):
	
	def __init__(self,x,y,name,id):
		self.type=4
		self.health=100
		self.att_pow=weaponList[name]
		self.healthreduction=weaponHealthList[name]
		self.pos=[x,y]
		self.name=name
		self.id=id
		
	def __repr__(self):
		return self.name + "(" + str(self.health)+ ")" 

@Singleton
class Grid:

	def __init__(self):
		self.n=1000
		self.pixels=[[Grass()]*self.n for i in range(self.n)]
		self.animals=[]
		self.player_id=-1
		self.lock=Lock()
		
	def loadMap(self,user):
		
		self.loadTrees(user)
		self.loadWeapons(user)
		self.loadAnimals(user)
		self.loadPlayer(user.username)
		self.loadUsers(user)

	def loadAnimals(self,user):
		db=MySQLdb.connect(host,usr,password,databaseName)
		cursor=db.cursor()
		cursor.execute("select * from Animals where animalPositionX between "+str(user.pos[0]-5)+" and "+str(user.pos[0]+5)+" and animalPositionY between "+str(user.pos[1]-5)+" and "+str(user.pos[1]+5)+";")
		db.commit()
		data=cursor.fetchall()
		for row in data:
			self.pixels[row[4]][row[5]]=Animal(row[4],row[5],row[7],row[1],row[0])
			self.animals.append(self.pixels[row[4]][row[5]])	
			self.pixels[row[4]][row[5]].attacked=row[6]
			self.pixels[row[4]][row[5]].health=row[3]
		db.close()

	def loadTrees(self,user):
		db=MySQLdb.connect(host,usr,password,databaseName)
		cursor=db.cursor()
		query="select * from Trees where treePosX between "+str(user.pos[0]-5)+" and "+str(user.pos[0]+5)+" and treePosY between "+str(user.pos[1]-5)+" and "+str(user.pos[1]+5)+";"
		
		cursor.execute(query)
		db.commit()
		data=cursor.fetchall()
		for row in data:
			self.pixels[row[3]][row[4]]=Tree(row[0])
			self.pixels[row[3]][row[4]].pos[0]=row[3]
			self.pixels[row[3]][row[4]].pos[1]=row[4]
			self.pixels[row[3]][row[4]].health=row[2]
		db.close()

	def loadWeapons(self,user):
		db=MySQLdb.connect(host,usr,password,databaseName)
		cursor=db.cursor()
		cursor.execute("select * from Weapons where weaponPositionX between "+str(user.pos[0]-5)+" and "+str(user.pos[0]+5)+" and weaponPositionY between "+str(user.pos[1]-5)+" and "+str(user.pos[1]+5)+" and weaponID not in( select weaponID from Inventories);")
		db.commit()
		data=cursor.fetchall()
		for row in data:
			self.pixels[row[4]][row[5]]=Weapon(row[4],row[5],row[1],row[0])	
			self.pixels[row[4]][row[5]].health=row[3]
		db.close()

	def loadPlayer(self,username):
		db=MySQLdb.connect(host,usr,password,databaseName)
		cursor=db.cursor()
		query="select * from Users where userName='"+username+"';"
		cursor.execute(query)
		db.commit()
		row=cursor.fetchall()
		row=row[0]

		self.player_id=row[0]
		self.pixels[row[4]][row[5]]=User(row[1],row[4],row[5],row[0])
		self.pixels[row[4]][row[5]].health=row[3]
		self.pixels[row[4]][row[5]].exp=row[7]
		self.pixels[row[4]][row[5]].lvl=row[8]
		self.pixels[row[4]][row[5]].color=row[9]
		self.pixels[row[4]][row[5]].direction=row[10]
		self.pixels[row[4]][row[5]].online=1
		cursor.execute("select * from Weapons where weaponID="+str(row[6])+";")
		db.commit()
		data2=cursor.fetchall()
		
		if data2:
			data2=data2[0]
			self.pixels[row[4]][row[5]].holding=Weapon(data2[4],data2[5],data2[1],data2[0])
			self.pixels[row[4]][row[5]].holding.health=data2[3]
		else:
			self.pixels[row[4]][row[5]].holding=Weapon(row[4],row[5],"Punch",-1)
		
		cursor.execute("select * from Inventories where invID="+str(row[0])+";")
		db.commit()
		data3=cursor.fetchall()
		for tmprow in data3:
			cursor.execute("select * from Weapons where weaponID="+str(tmprow[1])+";")
			db.commit()
			weapondata=cursor.fetchall()[0]
			weapon=Weapon(weapondata[4],weapondata[5],weapondata[1],weapondata[0])
			weapon.health=weapondata[3]
			self.pixels[row[4]][row[5]].inventory.append(weapon)
		db.close()
		return self.pixels[row[4]][row[5]]

	def loadUsers(self,user):
		db=MySQLdb.connect(host,usr,password,databaseName)
		try:
			
			cursor=db.cursor()
			cursor.execute("select * from Users where userID<>"+str(self.player_id)+" and userOnline="+str(1)+";")
			db.commit()
			data=cursor.fetchall()
			for row in data:
				self.pixels[row[4]][row[5]]=User(row[1],row[4],row[5],row[0])

				self.pixels[row[4]][row[5]].health=row[3]
				'''self.pixels[row[4]][row[5]].exp=row[7]'''
				self.pixels[row[4]][row[5]].lvl=row[8]
				self.pixels[row[4]][row[5]].color=row[9]
				'''self.pixels[row[4]][row[5]].direction=row[10]
				self.pixels[row[4]][row[5]].online=row[12]
				cursor.execute("select * from Weapons where weaponID="+str(row[6])+";")
				db.commit()
				data2=cursor.fetchall()

				if data2:
					data2=data2[0]
					self.pixels[row[4]][row[5]].holding=Weapon(data2[4],data2[5],data2[1],data2[0])
					self.pixels[row[4]][row[5]].holding.health=data2[3]
				else:
					self.pixels[row[4]][row[5]].holding=Weapon(row[4],row[5],"Punch",-1)'''
			db.close()
		except:
			db.close()

	def lakeRandomizer(self):
		query=Query()
		for i in range((self.n*2)/5,(self.n*4)/5):
			for t in range((self.n*2)/5,(self.n*4)/5):
				self.pixels[i][t]=Lake()

	def treeRandomizer(self):
		query=Query()
		for i in range(0,(self.n*self.n)/6):
			x=random.randint(0,(self.n)-1)
			y=random.randint(0,(self.n)-1)
			while(self.pixels[x][y].type!=1):
				x=random.randint(0,(self.n)-1)
				y=random.randint(0,(self.n)-1)
			
			self.pixels[x][y]=Tree(next(_id))
			self.pixels[x][y].pos[0]=x
			self.pixels[x][y].pos[1]=y
			query.addQuery(newTree(self.pixels[x][y]))
			query.executeQuery()
			query.emptyQuery()

	def animalRandomizer(self):
		query=Query()
		for i in range(0,(self.n*self.n)/20):
			x=random.randint(0,(self.n)-1)
			y=random.randint(0,(self.n)-1)
			while(self.pixels[x][y].type!=1):
				x=random.randint(0,(self.n)-1)
				y=random.randint(0,(self.n)-1)

			animal=animalList.keys()[random.randint(0,len(animalList)-1)]
			self.pixels[x][y]=Animal(x,y,animalList[animal],animal,next(_id))
			self.animals.append(self.pixels[x][y])	
			
			query.addQuery(newAnimal(self.pixels[x][y]))
			query.executeQuery()
			query.emptyQuery()

	def weaponRandomizer(self):
		query=Query()
		for i in range(0,(self.n*self.n)/20):
			x=random.randint(0,(self.n)-1)
			y=random.randint(0,(self.n)-1)
			while(self.pixels[x][y].type!=1):
				x=random.randint(0,(self.n)-1)
				y=random.randint(0,(self.n)-1)

			weapon=weaponList.keys()[random.randint(0,len(weaponList)-1)]
			if (weapon != 'Punch'):
				self.pixels[x][y]=Weapon(x,y,weapon,next(_id))
				
				query.addQuery(newWeapon(self.pixels[x][y]))
				query.executeQuery()
				query.emptyQuery()	
	def userRandomizer(self,username):
		query=Query()
		
		
		x=random.randint(0,(self.n)-1)
		y=random.randint(0,(self.n)-1)
		while(self.pixels[x][y].type!=1):
			x=random.randint(0,(self.n)-1)
			y=random.randint(0,(self.n)-1)
		db=MySQLdb.connect(host,usr,password,databaseName)
		cursor=db.cursor()
		cursor.execute("select max(userID) from Users;")
		db.commit()
		data=cursor.fetchall()
		data=data[0][0]
		print data
		if data != None:

			user=User(username,x,y,data+1)
		else:

			user=User(username,x,y,next(_id))
		db.close()
		self.pixels[x][y]=user	
		
		query.addQuery(newUser(user))
		query.executeQuery()
		query.emptyQuery()
		return user
	def createMap(self):

		self.lakeRandomizer()
		self.treeRandomizer()
		self.animalRandomizer()
		self.weaponRandomizer()
	def userMapAnimals(self,user):
		uanimals=[]

		for i in range(user.pos[0]-5,user.pos[0]+6):
			for t in range(user.pos[1]-5,user.pos[1]+6):
				try:
					if self.pixels[i][t].type==3:
						uanimals.append(self.pixels[i][t])
				except:
					continue
		print uanimals
		return uanimals
	def moveAnimals(self,user):
		message=[]
		query=Query()
		animals=self.userMapAnimals(user)
		if(user.online==1):
			for i in animals:
				try:
					i.animalMove()
					query.addQuery(updateAnimal(i))	
				except:
					message.append("Animal couldn't move")
					return message

	def printGrid(self):
		for i in range(0,self.n):
			for j in range(0,self.n):
				print self.pixels[i][j],
			print("\n"),
