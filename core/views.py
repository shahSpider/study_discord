from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'core/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, 'core/room.html', context)

def create_room(request):
    form = RoomForm()
    context = {'form': form}
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    return render(request, 'core/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('core:room', pk=room.id)
    context = {'form': form}

    return render(request, 'core/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=int(pk))
    if request.method == "POST":
        room.delete()
        return redirect('core:home')
    return render(request, 'core/delete.html', {'object': room})