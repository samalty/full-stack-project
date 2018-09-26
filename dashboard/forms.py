from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    
#    def clean(self):
#        """ Updates the project status based on the status of other fields """
#        if self.signed_off == True:
#            self.project_status == 'Done'
#        elif self.task1_status != 'To Do':
#            self.project_status == 'Doing'
#        else:
#            self.project_status == 'To Do'
#        return self.project_status
    
    class Meta:
        model = Project
        fields = ('project_title',
                  'description',
                  'client',
                  'fee',
                  'approved',
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
                  'task5_status',
                  'signed_off')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('task1_status',
                  'task2_status',
                  'task3_status',
                  'task4_status',
                  'task5_status',)