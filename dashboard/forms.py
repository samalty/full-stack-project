from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_title',
                  'description',
                  'client',
                  'fee',
                  'deadline',
                  'priority',
                  'task1',
                  'task1_status',
                  'task2',
                  'task2_status',
                  'task3',
                  'task3_status',
                  'task4',
                  'task4_status',
                  'task5',
                  'task5_status')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('task1_status',
                  'task2_status',
                  'task3_status',
                  'task4_status',
                  'task5_status',)

class EditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('description',
                  'fee',
                  'deadline',
                  'priority',
                  'task1',
                  'task2',
                  'task3',
                  'task4',
                  'task5',)

class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('description',
                  'deadline',
                  'task1',
                  'task2',
                  'task3',
                  'task4',
                  'task5',)