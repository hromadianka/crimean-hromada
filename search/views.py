from django.shortcuts import render
from django.db.models import Q
from project.models import Project, Task
from idea.models import Idea

# Create your views here.

def search(request):
    projects = []
    ideas = []
    tasks = []
    print(request.POST)

    if request.method == 'POST':
        search_input = request.POST.get('search-input')
        selected_types = request.POST.getlist('project-type')

        if not selected_types:  # If no specific type is selected, search across all types
            projects = Project.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))
            tasks = Task.objects.filter(Q(name__icontains=search_input))
            ideas = Idea.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))
        else:
            if 'project' in selected_types:
                projects = Project.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))

            if 'task' in selected_types:
                tasks = Task.objects.filter(Q(name__icontains=search_input))

                task_risk_filter = request.POST.getlist('project-risk')
                task_sphere_filter = request.POST.getlist('project-sphere')

                if task_risk_filter or task_sphere_filter:
                    if 'risk' in task_risk_filter:
                        tasks = tasks.filter(risk_level__in=task_risk_filter)
                    if 'sphere' in task_sphere_filter:
                        tasks = tasks.filter(activity_sphere__in=task_sphere_filter)

            if 'idea' in selected_types:
                ideas = Idea.objects.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))

        context = {
            'projects': projects,
            'ideas': ideas,
            'tasks': tasks,
            'no_results': False
        }

        print("Search input:", search_input)
        print("Selected types:", selected_types)

        # Перевірка, чи всі списки порожні
        if not (projects or ideas or tasks):
            context['no_results'] = True

        return render(request, 'results.html', context)

    return render(request, 'search.html')