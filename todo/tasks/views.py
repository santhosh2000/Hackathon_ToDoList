from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect #Add this
import pyrebase
import traceback
import time 

from .models import *
from .forms import *

# Global firebase config and variable
config = {
    "apiKey": "AIzaSyAt1UJNO-160UUjOcSEermiAFX32SpJOxA",
    "authDomain": "hackatonsecurity-project.firebaseapp.com",
    "databaseURL": "https://hackatonsecurity-project.firebaseio.com",
    "projectId": "hackatonsecurity-project",
    "storageBucket": "hackatonsecurity-project.appspot.com",
    "messagingSenderId": "642125821696",
    "appId": "1:642125821696:web:242be6a0f8fefdcd2ae5e5",
    "measurementId": "G-366W34KRWY"
  }
  
firebase = pyrebase.initialize_app(config)  
auth = firebase.auth()
db = firebase.database()


# Create your views here.

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation
def index(request):
	tasks = Task.objects.all()

	form = TaskForm()

	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')


	context = {'tasks':tasks, 'form':form}
	return render(request, 'tasks/list.html', context)

def signup(request):
	tasks = Task.objects.all()

	form = TaskForm()

	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')
	context = {'tasks':tasks, 'form':form, 'mesg': ''}
	return render(request, 'tasks/signup.html', context)
	
def welcome(request):
	tasks = Task.objects.all()

	form = TaskForm()

	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')


	context = {'tasks':tasks, 'form':form, 'mesg': ''}
	return render(request, 'tasks/index.html', context)

def updateTask(request, pk):
	task = Task.objects.get(id=pk)

	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}

	return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
	item = Task.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/')

	context = {'item':item}
	return render(request, 'tasks/delete.html', context)

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation	
def postLogin(request):
	print("inside postLogin..")
	username=request.POST.get('username')
	passw = request.POST.get("pass")
	try:
		user = auth.sign_in_with_email_and_password(username,passw)
	except:
		message="Invalid Login, please try again!"
		return render(request,"tasks/index.html",{"mesg":message})
	print(user['idToken'])
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	return render(request, "tasks/list.html",{"e":username})

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation	
def postSignup(request):

	name=request.POST.get('name')	
	username=request.POST.get('username')
	passw = request.POST.get("pass")
	try:
		user= auth.create_user_with_email_and_password(username,passw)
		print("inside postSignup..")
		data={"Name":name, "Username": username, "Password": passw ,"Date Created": time.strftime('%Y-%m-%d'), "Time Created":time.strftime('%H:%M:%S')}
		results = db.child("test").push(data, user['idToken'])
		print(results)
	except:
		print(traceback.print_exc())	
		message="Unable to create account User may already exist"
		return render(request,"tasks/signup.html",{"mesg":message})
	return render(request, "tasks/index.html",{"mesg":"%s successfully registered! Please login"%name})



