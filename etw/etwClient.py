from socket import *
from threading import *
import pickle
import os

host=""
port=9095
socket=socket(AF_INET,SOCK_STREAM)
socket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
socket.connect(("",9087))



choice=int(raw_input("1_New User\n2_Existing User\nEnter 1 or 2:"))
if choice==2:

	os.system('clear')
	username=raw_input("Enter a username:")
	message=[choice,username]
	try:
		socket.send(pickle.dumps(message))
	except:
		print "There is no user called "+username;
else:
	os.system('clear')
	username=raw_input("Enter a username:")
	message=[choice,username]
	try:
		socket.send(pickle.dumps(message))
	except:
		print "New user couldn't be created"
	
	
	#User Randomizer
	#user=mapa.userRandomizer(username)
class Receiver(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		while True:
			receive=socket.recv(8192)
			printMap(pickle.loads(receive))

	
def printMap(myMap):
	os.system('clear')
	for i in myMap:
		print i

receive=socket.recv(8192)
printMap(pickle.loads(receive))

while True:
	command=raw_input()
	try:

		socket.send(command)
		if(command=="exit"):
			print "BYE BYE..."
			break
		receive=socket.recv(8192)
		text=pickle.loads(receive)
		
		printMap(text)

	except:
		print "You are dead..."





