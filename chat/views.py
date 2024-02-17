
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from chat.models import Message
from django.contrib.auth.models import User
from userauths.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=request.user)
    active_chats = None
    chats = None
    profile = get_object_or_404(Profile, user=user)

    if messages:
        message = messages[0]
        active_chats = message['user'].username
        chats = Message.objects.filter(
            user=request.user, reciepient=message['user'])
        chats.update(is_read=True)

        for message in messages:
            if message['user'].username == active_chats:
                message['unread'] = 0
    context = {
        'chats': chats,
        'messages': messages,
        'active_chats': active_chats,
        'profile': profile,
    }
    return render(request, 'chat/messages.html', context)


@login_required
def chat_messages(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_chats = username
    chats = Message.objects.filter(user=user, reciepient__username=username)
    chats.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    context = {
        'chats': chats,
        'messages': messages,
        'active_chats': active_chats,
        # 'user_profile': user_profile,
        # 'friends_profile': friends_profile,
    }
    return render(request, 'chat/messages.html', context)


def send_message(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.sender_message(from_user, to_user, body)
        return redirect('inbox')


def UserSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
        context = {
            'users': users_paginator,
        }
    return render(request, 'chat/user_search.html', context)


def New_message(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('search')
    if from_user != to_user:
        Message.sender_message(from_user, to_user, body)
    return redirect('inbox')
