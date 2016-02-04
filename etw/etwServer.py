from socket import *
from threading import *
from etwClasses import *
import pickle
import os
import time

def runETW(user,command,lock,thread):
	
	query=Query()
	myMap=Grid()
	

	message=[]
	query.emptyQuery()
	
	if(command=="move"):
		message=  user.userMove(lock)
		
		

	elif(command=="attack"):
		try:
			message= user.userAttack(lock)
		except:

			message= [["You couldn't attack"]]
		
					
	elif(command.find("turn",0)!=-1):
		direction=command[5:]
		
		user.userChangeDirection(direction)
		
		
	elif(command=="cut"):
		try:
			message= user.userCutTree(lock)
		except:
			message= ["You couldn't hit the tree"]
		

	elif(command=="sleep"):
		user.sleep()
		

	elif(command=="take"):
		message= user.addToInventory(lock)
		

	elif(command.find("select",0)!=-1):
		name=command[7:]
		message= user.selectInventory(name)
		

	if(user.health <= 0):
		print "You are dead!"
		myMap.pixels[user.pos[0]][user.pos[1]] = Grass()
		query.addQuery(delUser(user))
		query.addQuery("Delete from Inventories where invID="+str(user.id)+";")
		for i in user.inventory:
			query.addQuery(delWeapon(i))
		query.executeQuery()
		query.emptyQuery()
		os.system("clear")
		print "You are dead..."
		return 
	elif(command=="exit"):
		user.online=0;
		myMap.pixels[user.pos[0]][user.pos[1]] = Grass()
		query.addQuery(updateUser(user)) 
		query.executeQuery()
		query.emptyQuery()

		print user.username+" has logged out.."

		os.system("clear")
		return "====== BYE BYE ======"
		
		
	query.executeQuery()
	return message
class AnimalMovement(Thread):
	def __init__(self,user):
		Thread.__init__(self)
		self.user=user
		self.signal=True
	def run(self):
		mapa=Grid()
		query=Query()

		while self.signal:
			t=0
			tmp=self.user.username
			self.user=mapa.loadPlayer(tmp)
			while(t!=10):
				for i in mapa.animals:
					if(i.attacked>0):
						i.attacked-=1
				time.sleep(1)
				t+=1

			mapa.moveAnimals(self.user)
			query.executeQuery()
	def terminate(self):
		self.signal=False		

def interface(user):

	myMap=Grid()
	myMap.loadMap(user)
	message=[]
	tmp=user.user_Map()
	for i in tmp:
		
		message.append(i)
	
	message.append("Username :"+str(user.username))
	message.append("Health :"+str(user.health))
	message.append("Direction :"+str(user.direction))
	message.append("Level :"+str(user.lvl))
	message.append("Exp :"+str(user.exp-lvlUpgrade[str(user.lvl)]))
	if (user.holding.name != 'Punch'):
		message.append("Weapon: "+str(user.holding.name)+"(%"+str(user.holding.health)+")")
	else:
		message.append("Weapon: "+str(user.holding.name))
	message.append("\nInventory:")
	message.append(user.printInv())
	return message

class mapLoader(Thread):
	def __init__(self,user):
		Thread.__init__(self)
		self.user=user
		self.signal=True
	def run(self):
		myMap=Grid()
		while self.signal:
			myMap.loadMap(self.user)
	def terminate(self):
		self.signal=False		


	
class commandCarrier(Thread):         
    def __init__(self,server,client,locks,_id):
		Thread.__init__(self)
		self.id=_id
		self.server = server
		self.client = client[0]
		self.locks=locks

    def run(self):
		startMessage=pickle.loads(self.client.recv(1024))
		print startMessage
		choice=startMessage[0]
		username=startMessage[1]
		
		if(choice==2):
			user=myMap.loadPlayer(username)
			user.online=1
			query.addQuery(updateUser(user))
			query.executeQuery()
		elif(choice==1):
			user=myMap.userRandomizer(username)
			user.online=0
			query.addQuery(updateUser(user))
			query.executeQuery()
			return
		socketList[user.id]=self.client
		
		myMap.loadMap(user)
		self.client.send(pickle.dumps(interface(user)))
		t=AnimalMovement(user)
		
		#loader.start()
		t.start()
		while True:
			try:
				before=user.health
				print username
				diff=[]
				
				command = self.client.recv(1024)
				print command
				user=myMap.loadPlayer(username)
				if(command=="exit"):
					runETW(user,command,None,self)
					t.terminate()
					t.join()
					break
				elif(command=="move"):
					message=runETW(user,command,self.locks[0],self)
					self.client.send(pickle.dumps(interface(user)+message+diff))
					
				elif(command=="attack"):
					print "attack start"
					message=runETW(user,command,self.locks[1],self)
					user=myMap.loadPlayer(username)
					print message
					if len(message)==2:
						print "attack birine"
						attackedUser=message[1]
						query.addQuery(updateUser(attackedUser))
						query.executeQuery()
						print str(attackedUser.health)+"======="
						message=[message[0]]
						print attackedUser.username,message,socketList[attackedUser.id]
					
						#socketList[attackedUser.id].send(pickle.dumps(interface(user)+[user.username+" has attacked you!!\n"+str(user.holding.att_pow+user.lvl*5)+" damaged received...\n"]))
					print "attack send edicek"
					self.client.send(pickle.dumps(interface(user)+message[0]+diff))
					print "attack send etti"
					
				elif(command=="cut"):
					message=runETW(user,command,self.locks[2],self)
					user=myMap.loadPlayer(username)
					self.client.send(pickle.dumps(interface(user)+message+diff))
					
				elif(command=="take"):
					message=runETW(user,command,self.locks[3],self)
					user=myMap.loadPlayer(username)
					self.client.send(pickle.dumps(interface(user)+message+diff))
					
				elif(command=="turn Right" or command=="turn Left" or command=="turn Up" or command=="turn Down"):

					message=runETW(user,command,None,self)
					user=myMap.loadPlayer(username)
					self.client.send(pickle.dumps(interface(user)+message+diff))

				elif(command.find("select",0)!=-1):
					message=runETW(user,command,None,self)
					user=myMap.loadPlayer(username)
					self.client.send(pickle.dumps(interface(user)+message+diff))
				elif(command=="sleep"):
					message=runETW(user,command,None,self)
					user=myMap.loadPlayer(username)
					self.client.send(pickle.dumps(interface(user)+message+diff))
				else:
					
					self.client.send(pickle.dumps(interface(user)))
				print command
			except:
				runETW(user,"exit",None,self) 
				print "Your command couldn't be executed..."

				break
			myMap.loadMap(user)
			user=myMap.loadPlayer(username)
			after=user.health
			if(before!=after):
				diff.append("You have been attacked!!")
				diff.append( str(before-after)+" damage received!!!!!")
		self.client.close()
		t.join()
		



port=9087
host=""
socket=socket(AF_INET,SOCK_STREAM)
socket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
socket.bind((host,port))
socket.listen(5)


#1.move
#2.attack
#3.cut
#4.take
locks = map(lambda x:Lock(), 4 * [None])
query=Query()
myMap=Grid()
myMap.lakeRandomizer()

socketList={}
userList={}
c = socket.accept()
print str(c)+" joined the game..."

thread_id=0
while c : 
	print "hop"
	a = commandCarrier(socket, c,locks,thread_id)
	thread_id+=1
	
	a.start()
	print "basladi"
	c = socket.accept()
	   
socket.close()
print hey


		