from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Project
from .forms import ProjectForm, TaskForm, EditForm, ClientEditForm

@login_required()
def user_dashboard(request):
    """ Renders the admin's dashboard and presents projects ordered by deadline """
    if not request.user.is_authenticated:
        raise Http404
    else:
        projects = Project.objects.filter(launched__lte=timezone.now()).order_by('deadline')
        return render(request, 'user_dashboard.html', {'projects': projects})

@login_required()
def launched(request):
    """ Presents projects ordered by launched date """
    if not request.user.is_authenticated:
        raise Http404
    else:
        projects = Project.objects.filter(launched__lte=timezone.now()).order_by('-launched')
        return render(request, 'user_dashboard.html', {'projects': projects})

@login_required()
def status(request):
    """ Presents projects ordered by project status """
    if not request.user.is_authenticated:
        raise Http404
    else:
        projects = Project.objects.filter(launched__lte=timezone.now()).order_by('-project_status')
        return render(request, 'user_dashboard.html', {'projects': projects})

@login_required()
def priority(request):
    """ Presents projects ordered by priority """
    if not request.user.is_authenticated:
        raise Http404
    else:
        projects = Project.objects.filter(launched__lte=timezone.now()).order_by('priority')
        return render(request, 'user_dashboard.html', {'projects': projects})

@login_required()
def project_detail(request, pk):
    """ Returns a single project based on its pk """
    if not request.user.is_authenticated:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(instance=project)
        context = {
            'form': form,
            'project': project,
            'task1_status': project.task1_status,
            'task2_status': project.task2_status,
            'task3_status': project.task3_status,
            'task4_status': project.task4_status,
            'task5_status': project.task5_status,
        }
        return render(request, 'project_detail.html', context)

@login_required()
def update_status(request, pk):
    """ Enables admin to edit the task status of projects """
    if not request.user.is_superuser:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        if request.method == "POST":
            form = TaskForm(request.POST, instance=project)
            if form.is_valid():
                project = form.save()
                project.save()
                print(project.task1_status)
                return redirect(project_detail, project.pk)
        else:
            form = TaskForm(instance=project)
        context = {
            'form': form,
            'project': project,
            'task1_status': project.task1_status,
            'task2_status': project.task2_status,
            'task3_status': project.task3_status,
            'task4_status': project.task4_status,
            'task5_status': project.task5_status,
        }
        return render(request, 'project_detail.html', context)

@login_required()
def plan_project(request, pk=None):
    if not request.user.is_superuser:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk) if pk else None
        if request.method == "POST":
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                project = form.save()
                project.save()
                return redirect(project_detail, project.pk)
        else:
            form = ProjectForm(instance=project)
        context = {
            'form': form,
            'project': project,
        }
        return render(request, 'plan_project.html', context)

@login_required()
def edit(request, pk):
    """ Allows users to edit certain form fields """
    if not request.user.is_authenticated:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        if request.user.is_superuser:
            if request.method == "POST":
                form = EditForm(request.POST, instance=project)
                if form.is_valid():
                    project = form.save()
                    project.save()
                    return redirect(project_detail, project.pk)
            else:
                form = EditForm(instance=project)
            context = {
                'form': form,
                'project': project,
            }
        else:
            if request.method == "POST":
                form = ClientEditForm(request.POST, instance=project)
                if form.is_valid():
                    project = form.save()
                    project.save()
                    return redirect(project_detail, project.pk)
            else:
                form = ClientEditForm(instance=project)
            context = {
                'form': form,
                'project': project,
            }
        return render(request, 'edit.html', context)

@login_required()
def delete_project(request, pk=None):
    """ Allows users to delete a project """
    if not request.user.is_superuser:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return redirect(reverse('user_dashboard'))

@login_required()
def approve_project(request, pk):
    """ Allows users to approve a project """
    if not request.user.is_authenticated:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        project.approved=True
        project.save()
        return redirect(project_detail, project.pk)

@login_required()
def sign_off(request, pk):
    """ Allows users to sign a project off """
    if not request.user.is_authenticated:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        project.signed_off=True
        project.save()
        return redirect(project_detail, project.pk)