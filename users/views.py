from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from users.models import Profile
from project.models import Project
from idea.models import Idea 

# Create your views here.

def custom_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        link = request.POST.get('link')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'register.html', {'error': 'Паролі не співпадають'})

        # Використовуємо create_user замість створення користувача та збереження паролю
        user = User.objects.create_user(username=username, password=password1)

        # Створення профілю для користувача
        profile = Profile(user=user, name=username, chat_element=link, description='')
        profile.save()

        # Автоматичний вхід після реєстрації
        auth.login(request, user)

        return redirect('/')

    return render(request, 'register.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Wrong password or username'})

    return render(request, 'login.html')


def custom_logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='login')
def account(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user.id)
    print(profile)

    created_projects = Project.objects.filter(author=user)
    created_ideas = Idea.objects.filter(author=user)
    saved_ideas = profile.saved_ideas.all()

    context = {
        'profile': profile,
        'created_projects': created_projects,
        'created_ideas': created_ideas,
        'saved_ideas': saved_ideas,
    }
    return render(request, 'account.html', context)

@login_required(login_url='login')
def edit_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile

    if request.user != user:
        raise PermissionDenied("You do not have permission to edit this profile.")

    if request.method == 'POST' and request.user == user:
        new_description = request.POST.get('content')
        new_chat_element = request.POST.get('chat_element')
        
        profile.description = new_description
        profile.chat_element = new_chat_element
        profile.save()

        return redirect('account', user_id=user.id)

    return render(request, 'account.html', {'profile': profile})