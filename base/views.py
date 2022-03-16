from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Topic
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .form import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
# rooms = [
#     {'id':1, 'name':'Lets learn Python'},
#     {'id':2, "name":"Lets learn UI"},
#     {'id':3, "name":"Hello WOrld"},
# ]

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exists')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exists')
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # this searches upwards. From Room model to TOpic name model. Therefore double underscores used
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |    #now we can search for 3 different values. for topic name, for name and description. Q is used to chain queries
        Q(description__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # this sets the initial values of form to the values retrived from database
    if request.user != room.host:
        return HttpResponse("Not allowed")
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) # this means, the data in request will replace data of room with id pk
        if form.is_valid():
            form.save()
            return redirect('home')
    context= {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Not allowed")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj': room})