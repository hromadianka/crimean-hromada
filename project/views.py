from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .models import Project, Resource, Task
from users.models import Profile


# Create your views here.

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
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.author:
        raise PermissionDenied("You do not have permission to edit this project.")

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
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.author:
        raise PermissionDenied("You do not have permission to delete this project.")

    if request.method == 'POST':
        project.delete()
        return redirect('/') 

    return render(request, 'delete_project.html', {'project': project})

@login_required(login_url='/login')
def add_resource_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.author:
        raise PermissionDenied("You do not have permission to add resources to this project.")

    if request.method == 'POST':
        resource_name = request.POST.get('resource_name')
        resource = Resource.objects.create(name=resource_name)
        project.resources.add(resource)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url='/login')
def add_task_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.author:
        raise PermissionDenied("You do not have permission to add tasks to this project.")

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_risk_level = request.POST.get('task_risk_level')
        task_activity_sphere = request.POST.get('task_activity_sphere')

        task = Task.objects.create(
            name=task_name,
            risk_level=task_risk_level,
            activity_sphere=task_activity_sphere,
        )
        project.tasks.add(task)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url='/login')
def edit_resource(request):


    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        new_name = request.POST.get('new_name')

        resource = get_object_or_404(Resource, id=resource_id)
        projects = Project.objects.filter(resources=resource)

        if not any(request.user == project.author for project in projects):
            raise PermissionDenied("You do not have permission to edit this resource.")


        resource.name = new_name
        resource.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url='/login')
def delete_resource(request):
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')

        resource = get_object_or_404(Resource, id=resource_id)
        projects = Project.objects.filter(resources=resource)

        if not any(request.user == project.author for project in projects):
            raise PermissionDenied("You do not have permission to delete this resource.")


        resource.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required(login_url='/login')
def edit_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_name = request.POST.get('new_name')

        task = get_object_or_404(Task, id=task_id)

        projects = Project.objects.filter(tasks=task)

        if not any(request.user == project.author for project in projects):
            raise PermissionDenied("You do not have permission to edit this task.")


        task.name = new_name
        task.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required(login_url='/login')
def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        task = get_object_or_404(Task, id=task_id)

        projects = Project.objects.filter(tasks=task)
        if not any(request.user == project.author for project in projects):
            raise PermissionDenied("You do not have permission to delete this task.")

        task.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required(login_url='login')
def save_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=user)

            if project not in profile.favorite_projects.all():
                profile.favorite_projects.add(project)
                project.likes += 1
                project.save()
                updated_likes = project.likes
                return JsonResponse({'success': True, 'message': 'Project saved successfully.', 'likes': updated_likes})
            else:
                profile.favorite_projects.remove(project)
                project.likes -= 1
                project.save()
                updated_likes = project.likes
                return JsonResponse({'success': True, 'message': 'Project removed from favorited projects.', 'likes': updated_likes})
           

        else:
            return JsonResponse({'success': False, 'message': 'User is not authenticated.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

