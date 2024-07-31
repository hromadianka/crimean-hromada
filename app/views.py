from django.shortcuts import render, redirect, get_object_or_404
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Project, Idea, Task, Resource, News
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from project.models import Project, Task
from idea.models import Idea


# Create your views here.

def index(request):
    return render(request, 'index.html')

def map(request):
    return render(request, 'map.html')



@login_required(login_url='/login')
def publish(request):
    ideas = Idea.objects.all()

    if request.method == 'POST':
        choice = request.POST.get('choice')
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if choice == 'project':
            chat_element_project = request.POST.get('chat_element_project')
            idea_id = request.POST.get('idea_id')

            # Перевірка, чи передана ідея
            if idea_id:
                idea = Idea.objects.get(id=idea_id)
            else:
                idea = None

            project = Project.objects.create(
                name=name,
                description=description,
                chat_element=chat_element_project,
                author=request.user
            )

            # Перевірка, чи ідея передана та пов'язана з проєктом
            if idea:
                project.ideas.add(idea)

            return redirect('project', project_id=project.id)
        elif choice == 'idea':
            idea = Idea.objects.create(
                name=name,
                description=description,
                author=request.user
            )
            return redirect('idea_detail', idea_id=idea.id)
    
    return render(request, 'publish.html', {'ideas': ideas})

@login_required(login_url='/login')
def publish_with_idea(request, idea_id):
    idea = Idea.objects.get(id=idea_id)

    if request.method == 'POST':
        # Логіка публікації проєкту за ідеєю
        name = request.POST.get('name')
        description = request.POST.get('description')
        chat_element_project = request.POST.get('chat_element_project')

        project = Project.objects.create(
            name=name,
            description=description,
            chat_element=chat_element_project,
            author=request.user
        )
        project.ideas.add(idea)  # Підв'язуємо ідею до проєкту

        return redirect('project', project_id=project.id)

    return render(request, 'publish.html', {'idea': idea})

def self_government(request):
    return render(request, 'self_government.html')
