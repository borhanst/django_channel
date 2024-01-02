from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.


def home(request):
    # message = Message.objects.filter(room='mnA32h').filter(Q(sender=1) | Q(sender=2)).values("group_name", "room").distinct()
    # print(message)
    return render(request, "home.html")


def room(request, room_id=None):
    # rev_id = request.GET.get('id')
    # chat_type = request.GET.get('type')
    # group_name = request.GET.get('name')
    # if room_id is None:
    #     room_id = str(uuid.uuid4())[0:6]
    # chat, created = Chat.objects.get_or_create(chat_id=room_id)

    # if created and not chat_type:
    #     chat.admin = request.user
    #     chat.customer = User.objects.get(id=rev_id)
    #     chat.save()
    # if chat_type:
    #     chat_type.chat_type = chat_type
    #     chat.members.add(request.user)
    #     chat.group = group_name
    # print(chat)
    # message = Message.objects.filter(room='mnA32h')
    return render(request, "room.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print('login error', user)
    
    return render(request, 'login.html')