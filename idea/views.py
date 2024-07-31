
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .models import Idea
from users.models import Profile


# Create your views here.

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

@login_required(login_url='/login')
def save_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=user)  # Отримуємо або створюємо профіль
            if idea not in profile.saved_ideas.all():
                profile.saved_ideas.add(idea)
                return JsonResponse({'success': True, 'message': 'Idea saved successfully.'})
            else:
                profile.saved_ideas.remove(idea)
                return JsonResponse({'success': True, 'message': 'Idea removed from saved ideas.'})
        else:
            return JsonResponse({'success': False, 'message': 'User is not authenticated.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
