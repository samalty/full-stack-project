from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Project
from .forms import ProjectForm, TaskForm

def user_dashboard(request):
    """ Renders the admin's dashboard """
    if not request.user.is_superuser:
        raise Http404
    else:
        projects = Project.objects.filter(launched__lte=timezone.now()).order_by('-launched')
        return render(request, 'user_dashboard.html', {'projects': projects})

def client_dashboard(request):
    """ Renders the client's dashboard """
    projects = Project.objects.filter(launched__lte=timezone.now()).order_by('-launched')
#    projects = Project.objects.filter(project.client=current_user.username).all()
    return render(request, 'client_dashboard.html', {'projects': projects})

def project_detail(request, pk):
    """ Returns a single project based on its pk """
    if not request.user.is_superuser:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        if request.method == "POST":
            """ Enables admin to edit the task status of projects """
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                project = form.save()
                project.save()
#                return redirect(project_detail, project.pk)
                return HttpResponseRedirect(project.get_absolute_url())
        else:
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

def delete_project(request, pk=None):
    """ Allows users to delete a project """
    if not request.user.is_superuser:
        raise Http404
    else:
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return redirect(reverse('user_dashboard'))

def client_project_detail(request, pk):
    """ Returns a single project based on its pk """
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'client_project_detail.html', {'project': project})

def approve_project(request, pk):
    """ Allows users to approve a project """
    project = get_object_or_404(Project, pk=pk)
    project.approved=True
    project.save()
    return redirect(client_project_detail, project.pk)

def sign_off(request, pk):
    """ Allows users to sign a project off """
    project = get_object_or_404(Project, pk=pk)
    project.signed_off=True
    project.save()
    return redirect(client_project_detail, project.pk)