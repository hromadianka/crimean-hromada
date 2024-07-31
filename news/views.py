
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import News
from project.models import Project

# Create your views here.

def news_detail(request, project_id, news_id):
    project = get_object_or_404(Project, id=project_id)
    news = get_object_or_404(News, id=news_id)

    return render(request, 'news_detail.html', {'project': project, 'news': news})

@login_required(login_url='login')
def edit_news(request, project_id, news_id):

    project = get_object_or_404(Project, id=project_id)
    if request.user != project.author:
        raise PermissionDenied("You do not have permission to delete this news.")

    news = get_object_or_404(News, id=news_id)

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
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.author:
        raise PermissionDenied("You do not have permission to delete this news.")

    news = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        news.delete()
        return redirect('project', project_id=project_id)

    return render(request, 'delete_news.html', {'news': news, 'project_id': project_id, 'news_id': news_id})

@login_required(login_url='login')
def add_news(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.author:
        raise PermissionDenied("You do not have permission to add news to this project.")

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Створення новини і збереження в базі даних
        news = News.objects.create(
            title=title,
            content=content,
        )

        project.news.add(news)


        return redirect('project', project_id=project_id)

    return render(request, 'add_news.html', {'project': project})
