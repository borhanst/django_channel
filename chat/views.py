from django.shortcuts import render, redirect
from chat.models import Chat
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import authenticate, login
from django.db.models import Q
# Create your views here.


def home(request):
    chats = Chat.objects.filter(Q(admin=request.user) | Q(customer=request.user))
    # chats_id = chats.members.values_list('id', flat=True)
    users = User.objects.exclude(id=request.user.id)
    group_chats = Chat.objects.filter(members=request.user)
    print(chats)
    return render(request, "home.html", {"users": users, "chats": chats, "group_chats": group_chats})


def room(request, room_id=None):
    rev_id = request.GET.get('id')
    chat_type = request.GET.get('type')
    group_name = request.GET.get('name')
    if room_id is None:
        room_id = str(uuid.uuid4())[0:6]
    chat, created = Chat.objects.get_or_create(chat_id=room_id)

    if created and not chat_type:
        chat.admin = request.user
        chat.customer = User.objects.get(id=rev_id)
        chat.save()
    if chat_type:
        chat_type.chat_type = chat_type
        chat.members.add(request.user)
        chat.group = group_name
    print(chat)
    return render(request, "room.html", {"room_name": chat.chat_id, "chat": chat})


def login_view(request):
    print(request.POST)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    
    return render(request, 'login.html')