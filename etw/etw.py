from etwClasses import *
import threading 
import os
import time
#Exiled To Wild
#Authors: Enver Evci, Onat Buyukakkus


class AnimalMovement(Thread):
	def run(self):

		while True:
			t=0
			while(t!=10):
				for i in mapa.animals:
					if(i.attacked>0):
						i.attacked-=1
				time.sleep(1)
				t+=1

			mapa.moveAnimals(user)
			
		
class UserMap(Thread):
	def run(self):
		while True:
			os.system('clear')
			user.user_Map()
			print "Username :"+str(user.username)
			print "Health :"+str(user.health)
			print "Direction :"+str(user.direction)
			print "Level :"+str(user.lvl) 
			print "Exp :"+str(user.exp-lvlUpgrade[str(user.lvl)])
			if (user.holding.name != 'Punch'):
				print "Weapon: "+str(user.holding.name)+"(%"+str(user.holding.health)+")"
			else:
				print "Weapon: "+str(user.holding.name) 
			print "\nInventory:"
			print user.printInv()
			time.sleep(10)
	



'''
start=int(raw_input("1_New Game\n2_Continue\nEnter 1 or 2:"))

if start==2:

	choice=int(raw_input("1_New User\n2_Existing User\nEnter 1 or 2:"))
	if choice==2:

		os.system('clear')
		username=raw_input("Enter a username:")
		mapa=Grid()
		mapa.loadMap()
		query=Query()
		try:
			user=mapa.loadPlayer(username)
			t2=Command()
			t3=UserMap()
			t1=AnimalMovement()
			t1.start()
			t2.start()
			t3.start()
		except:
			print "There is no user called "+username;
	else:
		os.system('clear')
		username=raw_input("Enter a username:")
		mapa=Grid()
		mapa.loadMap()
		query=Query()
		
		#User Randomizer
		user=mapa.userRandomizer(username)
		
		t2=Command()
		t3=UserMap()
		t1=AnimalMovement()
		t1.start()
		t2.start()
		t3.start()
		
	
else:
	os.system('python emptyTables.py')
	username=raw_input("Enter a username:")
	mapa=Grid()
	mapa.createMap()
	query=Query()
	t1,t2,t3=0,0,0
	user=mapa.userRandomizer(username)
	
	

	t2=Command()
	t3=UserMap()
	t1=AnimalMovement()
	t1.start()
	t2.start()
	t3.start()
'''