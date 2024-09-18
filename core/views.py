from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q

def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Username or Password are incorrect')
    context = {'page': page}
    return render(request, 'core/login_register.html', context)

def logout_view(request):
    logout(request)
    return redirect('core:home')

def register_user(request):
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'form': form}
    return render(request, 'core/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.all()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'core/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_chat = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        Message.objects.create(
            user = request.user,
            room = room,
            body=request.POST.get("body"),
        )
        room.participants.add(request.user)
        return redirect('core:room', pk=room.id)
    context = {
        "room": room,
        "room_chat": room_chat,
        "participants": participants,    
    }
    return render(request, 'core/room.html', context)

@login_required(login_url='login/')
def create_room(request):
    form = RoomForm()
    context = {'form': form}
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    return render(request, 'core/room_form.html', context)

@login_required(login_url='/login/')
def update_room(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You're not allowed here")
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('core:room', pk=room.id)
    context = {'form': form}

    return render(request, 'core/room_form.html', context)

@login_required(login_url='/login/')
def delete_room(request, pk):
    room = Room.objects.get(id=int(pk))
    if not(request.user == room.host or request.user.is_superuser):
        return HttpResponse("You're not allowed to delete")

    if request.method == "POST":
        room.delete()
        return redirect('core:home')
    return render(request, 'core/delete.html', {'object': room})

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=int(pk))
    if not(request.user == message.user or request.user.is_superuser):
        return HttpResponse("You're not allowed to delete this message")
    
    if request.method == "POST":
        message.delete()
        return redirect('core:home')
    return render(request, 'core/delete.html', {'object': message})