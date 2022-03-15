from django.shortcuts import render, redirect
from .models import Room, Topic
from .form import RoomForm
# Create your views here.
# rooms = [
#     {'id':1, 'name':'Lets learn Python'},
#     {'id':2, "name":"Lets learn UI"},
#     {'id':3, "name":"Hello WOrld"},
# ]
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # this searches upwards. From Room model to TOpic name model. Therefore double underscores used
    rooms = Room.objects.filter(topic__name__icontains=q)
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics}
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # this sets the initial values of form to the values retrived from database
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) # this means, the data in request will replace data of room with id pk
        if form.is_valid():
            form.save()
            return redirect('home')
    context= {'form':form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj': room})