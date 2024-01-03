from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
import uuid
from chat.models import Room, Message
# Create your views here.


def home(request, pk):
    groups = Room.objects.filter(store=1, is_group=True, message__sender=pk)
    rooms = (
        Room.objects.filter(store=2, is_group=False)
        .values("message__sender", "room_id")
        .distinct("message__sender")
    )
    room_list = (
        Room.objects.filter(store=2, is_group=False)
        .values_list("message__sender", flat=True)
        .distinct("message__sender")
    )
    context = {"groups": groups, "rooms": rooms, "pk": pk, 'room_list': room_list}
    return render(request, "home.html", context)


def room(request, pk, room_id=None):
    

    if room_id is None:
        room_id = uuid.uuid4()
        room = Room.objects.create(room_id=room_id)

        room.is_group = False
        room.store = 2
        
        room.save()
        user = 2 if pk == 1 else 1
        
        message_obj = [
            Message(
                sender=pk,
                event_type="room_create",
                body=f"start chat with {user}",
                room=room,
            ),
            Message(
                sender=user,
                event_type="add_room",
                body=f"start chat with {pk}",
                room=room,
            ),
        ]

        messages = Message.objects.bulk_create(message_obj)
    else:
        messages = Message.objects.filter(room__room_id=room_id)
    context = {"messages": messages, "pk": pk, "room_name": room_id}
    return render(request, "room.html", context)

def group_create(request, pk):
    group_name = request.GET.get('name')
    room_id = uuid.uuid4()
    room = Room.objects.create(room_id=room_id)

    
    room.is_group = True
    room.group_display_name=group_name
    room.store = 1
    
    
    room.save()
    msg = Message(
        sender=pk,
        event_type="group_create",
        body=f"{pk} create this group",
        room=room,
    )
    msg.save()
    return redirect(reverse_lazy('chat_room', kwargs={'room_id': room.room_id, 'pk': pk}))

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            print("login error", user)

    return render(request, "login.html")
