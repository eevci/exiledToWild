from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from django.template import RequestContext, loader,Context
from django.core.context_processors import csrf
from socket import *
from threading import *
import pickle
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import models
import simplejson as json
from forms.forms import PostForm
import datetime
host=""
port=9095
sockets={}
sock=[]


def index(request):
	return redirect("/login")


def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	return HttpResponse(html)
def login_view(request):

	return render(request,'login.html')	
def post_form_upload(request):
	if request.method == 'GET':
		form = PostForm()
	else:
		# A POST request: Handle Form Upload
		form = PostForm(request.POST) # Bind data from request.POST into a PostForm
 
		# If data is valid, proceeds to create a new post and redirect the user
		if form.is_valid():
			content = form.cleaned_data['content']
			created_at = form.cleaned_data['created_at']
			post = m.Post.objects.create(content=content,
										 created_at=created_at)
			return HttpResponseRedirect(reverse('post_detail',
												kwargs={'post_id': post.id}))
 
	return render(request, 'post_form_upload.html', {
		'form': form,
	})
def login_post(request):
	
	username = request.POST['username']
	password = request.POST['password']
	user= authenticate(username=username,password=password)  
	if(user is not None):
		if user.is_active:
			
			login(request, user)
			tmp=socket(AF_INET,SOCK_STREAM)
			tmp.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
			tmp.connect(("",9087))
			message=[2,username]
			tmp.send(pickle.dumps(message))
			
			sockets[username]=tmp
			receive=sockets[username].recv(8192)
			text=pickle.loads(receive)
			render(request,'home.html',{'username':request.user.username,'lastlogin':request.user.last_login,'lastcommand':"None",'map':text})
			return redirect("/home")
		else:
			return render(request, 'login.html', {'message':'Account is disabled'})
	else:
		
		return redirect("/login")

def home(request):

	if  not request.user.is_authenticated():
		return redirect("/login")
	if request.method =='GET':
		pass
	elif request.method =='POST':

		
		command=request.POST['command']
		sockets[request.user.username].send(command)
		receive=sockets[request.user.username].recv(8192)
		text=pickle.loads(receive)


		if(text!="1"):
			return render(request,'home.html',{'username':request.user.username,'lastlogin':request.user.last_login,'lastcommand':command})
	return render(request,'home.html',{'username':request.user.username,'lastlogin':request.user.last_login})
def success(obj, name):
	return HttpResponse(json.dumps({'result':'Success',name : obj}),
				'text/json')
def error(reason):
	return HttpResponse(json.dumps({'result':'Fail','reason' : reason}),
				'text/json')
def getMap(request):
	if request.method =='POST':

		try:
			command=request.POST['command']
			
		except:
			command="a"
		sockets[request.user.username].send(command)
		receive=sockets[request.user.username].recv(8192)
		text=pickle.loads(receive)
		
	else:
		command="a"
		sockets[request.user.username].send(command)
		receive=sockets[request.user.username].recv(8192)
		text=pickle.loads(receive)
	return success(text,'interf')
def sign_view(request):
	context = Context({"message": ""})
	try:
		context.update({'message': request.GET['msg']})
	except:
		pass
	return render(request,'sign_up.html',context)
def sign_post(request):
	p = request.POST
	dt = datetime.datetime.now()
	if(p['username'] and p['firstname'] and p['lastname'] and p['email'] and p['password'] ):
		if(p['password'] == p['cpassword']):
			user = User.objects.create_user(password=p['password'], username=p['username'],
				first_name=['firstname'], last_name=p['lastname'], email=p['email'])
			tmp=socket(AF_INET,SOCK_STREAM)
			tmp.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
			tmp.connect(("",9087))
			message=[1,p['username']]
			tmp.send(pickle.dumps(message))
			
			return redirect("/login")

		else:
			
			return HttpResponseRedirect('/sign-up/?msg="Passwords don\'t match"')
			#return render(request,'sign_up.html',{'message':"Passwords don't match"})
	else:
		
		return HttpResponseRedirect('/sign-up/?msg="Fields cannot be empty"')
		

		
def logout_view(request):
	
	sockets[request.user.username].send("exit")
	sockets[request.user.username].close()
	del sockets[request.user.username]
	logout(request)
	return redirect("/login")
	