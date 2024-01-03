from django.shortcuts import render, get_object_or_404
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Project, Idea, Task, Resource, News
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
import random
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout




# Create your views here.

def index(request):
    return render(request, 'index.html')

def map(request):
    return render(request, 'map.html')

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

def search(request):
    projects = []
    ideas = []
    tasks = []

    if request.method == 'POST':
        search_input = request.POST.get('search-input')
        selected_types = request.POST.getlist('project-type')

        if 'project' in selected_types:
            projects = Project.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))

        if 'task' in selected_types:
            tasks = Task.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))
    
            task_risk_filter = request.POST.getlist('project-risk')
            task_sphere_filter = request.POST.getlist('project-sphere')

            if task_risk_filter or task_sphere_filter:
                for filter_type in task_risk_filter + task_sphere_filter:
                    if filter_type == 'risk':
                        tasks = tasks.filter(risk_level__in=task_risk_filter)
                    elif filter_type == 'sphere':
                        tasks = tasks.filter(activity_sphere__in=task_sphere_filter)
  

        if 'idea' in selected_types:
            ideas = Idea.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))

        context = {
            'projects': projects,
            'ideas': ideas,
            'tasks': tasks,
            'no_results': False
        }
        
        # Перевірка, чи всі списки порожні
        if not (projects or ideas or tasks):
            context['no_results'] = True

        return render(request, 'results.html', context)

    return render(request, 'search.html')



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
            return redirect('idea', idea_id=idea.id)
    
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

def wiki(request):
    return render(request, 'wiki.html')

def self_government(request):
    return render(request, 'self_government.html')

def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    related_ideas = project.ideas.all()

    if request.user == project.author:
        is_author = True
    else:
        is_author = False

    return render(request, 'project.html', {'project': project, 'is_author': is_author, 'related_ideas': related_ideas})

@login_required(login_url='login')
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user != project.author:
        return redirect('project', project_id=project_id)

    if request.method == 'POST':
        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.chat_element = request.POST.get('chat_element_project')
        project.save()
        return redirect('project', project_id=project_id)

    return render(request, 'edit_project.html', {'project': project})

@login_required(login_url='login')
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.author:
        return redirect('project', pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('/') 

    return render(request, 'delete_project.html', {'project': project})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        link = request.POST.get('link')

        user = Profile.objects.create_user(username=username, password=password)
        profile = Profile(user=user, chat_element=link)
        profile.save()

        login(request, user)
        return redirect('profile')

    return render(request, 'register.html')

@login_required(login_url='login')
def account(request, user_id):
    user = get_object_or_404(User, id=user_id)
    print(f"User ID: {user.id}")

    profile = get_object_or_404(Profile, user=user)
    print(f"Profile User ID: {profile.user.id}")

    created_projects = profile.created_projects.all()
    created_ideas = Idea.objects.filter(author=user)
    saved_ideas = profile.saved_ideas.all()

    context = {
        'profile': profile,
        'created_projects': created_projects,
        'created_ideas': created_ideas,
        'saved_ideas': saved_ideas,
    }
    return render(request, 'account.html', context)



def news_detail(request, project_id, news_id):
    project = get_object_or_404(Project, id=project_id)
    news = get_object_or_404(News, id=news_id)

    return render(request, 'news_detail.html', {'project': project, 'news': news})

@login_required(login_url='login')
def edit_news(request, project_id, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.user != news.author:
        return redirect('news_detail', project_id=project_id, news_id=news_id)

    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')

        # Оновлення зображення, якщо нове зазначене в POST-даних
        new_image = request.FILES.get('image')
        if new_image:
            # Видаляємо старе зображення, якщо воно є
            if news.image:
                default_storage.delete(news.image.path)

            # Зберігаємо нове зображення
            image_name = f"news_images/{project_id}/{news_id}/{new_image.name}"
            news.image = ContentFile(new_image.read())
            news.image.name = image_name

        news.save()
        return redirect('news_detail', project_id=project_id, news_id=news_id)

    return render(request, 'edit_news.html', {'news': news, 'project_id': project_id, 'news_id': news_id})

@login_required(login_url='login')
def delete_news(request, project_id, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.user != news.author:
        return redirect('news_detail', project_id=project_id, news_id=news_id)

    if request.method == 'POST':
        news.delete()
        return redirect('project', project_id=project_id)

    return render(request, 'delete_news.html', {'news': news, 'project_id': project_id, 'news_id': news_id})

@login_required(login_url='login')
def add_news(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Обробка завантаження зображення
        image = request.FILES.get('image')

        # Створення новини і збереження в базі даних
        news = News.objects.create(
            title=title,
            content=content,
            image=image,
            project=project,
            author=request.user
        )

        return redirect('project', project_id=project_id)

    return render(request, 'add_news.html', {'project': project})

@login_required(login_url='/login')
def add_resource_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        resource_name = request.POST.get('resource_name')
        resource = Resource.objects.create(name=resource_name)
        project.resources.add(resource)
        return JsonResponse({'success': True, 'resource_id': resource.id})

    return JsonResponse({'success': False})

@login_required(login_url='/login')
def edit_resource(request):
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        new_name = request.POST.get('new_name')

        resource = get_object_or_404(Resource, id=resource_id)
        resource.name = new_name
        resource.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url='/login')
def delete_resource(request):
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')

        resource = get_object_or_404(Resource, id=resource_id)
        resource.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url='/login')
def add_task_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        task_risk_level = request.POST.get('task_risk_level')
        task_activity_sphere = request.POST.get('task_activity_sphere')

        task = Task.objects.create(
            name=task_name,
            description=task_description,
            risk_level=task_risk_level,
            activity_sphere=task_activity_sphere,
            project=project
        )
        project.tasks.add(task)
        return JsonResponse({'success': True, 'task_id': task.id})

    return JsonResponse({'success': False})


@login_required(login_url='/login')
def edit_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_name = request.POST.get('new_name')
        new_description = request.POST.get('new_description')
        new_risk_level = request.POST.get('new_risk_level')
        new_activity_sphere = request.POST.get('new_activity_sphere')

        task = get_object_or_404(Task, id=task_id)
        task.name = new_name
        task.description = new_description
        task.risk_level = new_risk_level
        task.activity_sphere = new_activity_sphere
        task.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required(login_url='/login')
def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        task = get_object_or_404(Task, id=task_id)
        task.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url='login')
def edit_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile

    if request.method == 'POST' and request.user == user:
        new_description = request.POST.get('content')
        new_chat_element = request.POST.get('chat_element')
        
        profile.description = new_description
        profile.chat_element = new_chat_element
        profile.save()

        return redirect('account', user_id=user.id)

    return render(request, 'account.html', {'profile': profile})

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    projects = idea.projects.all()

    return render(request, 'idea.html', {'idea': idea, 'projects': projects})

@login_required(login_url='login')
def idea_edit(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, author=request.user)

    if request.method == 'POST':
        idea.name = request.POST.get('name')
        idea.description = request.POST.get('description')
        idea.save()
        return redirect('idea_detail', idea_id=idea.id)

    return render(request, 'idea_edit.html', {'idea': idea})


@login_required(login_url='login')
def idea_delete(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, author=request.user)

    if request.method == 'POST':
        idea.delete()
        return redirect('/')  # Замініть 'your_redirect_url' на той URL, на який ви хочете перенаправити після видалення ідеї

    return render(request, 'idea_delete.html', {'idea': idea})

@login_required(login_url='login')
@require_POST
def toggle_favorite(request, project_id):
    project = Project.objects.get(id=project_id)
    project.toggle_favorite(request.user)
    return JsonResponse({'likes': project.likes, 'favorited': request.user in project.favorited_by})

@login_required(login_url='/login')
def save_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.method == 'POST':
        user = request.user
        if user not in idea.saved_by.all():
            idea.saved_by.add(user)
            return JsonResponse({'success': True, 'message': 'Idea saved successfully.'})
        else:
            idea.saved_by.remove(user)
            return JsonResponse({'success': True, 'message': 'Idea removed from saved ideas.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})