from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

class Project(models.Model):
    """ Model for individual project plans """
    urgency = (
        ('1', 'High'),
        ('2', 'Medium'),
        ('3', 'Low'),
    )
    status = (
        ('To Do', 'To Do'),
        ('Doing', 'Doing'),
        ('Done', 'Done'),
    )
    project_title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    fee = models.DecimalField(blank=False, max_digits=6, decimal_places=2)
    plus_vat = models.DecimalField(blank=False, max_digits=6, decimal_places=2)
    launched = models.DateTimeField(blank=True, null=True, default=timezone.now)
    approved = models.BooleanField(blank=False, default=False)
    deadline = models.DateField(blank=False)
    priority = models.CharField(max_length=6, choices=urgency, blank=False)
    task1 = models.CharField(max_length=200, blank=False)
    task1_status = models.CharField(max_length=5, choices=status, blank=False, default='To Do')
    task2 = models.CharField(max_length=200, blank=True)
    task2_status = models.CharField(max_length=5, choices=status, blank=True)
    task3 = models.CharField(max_length=200, blank=True)
    task3_status = models.CharField(max_length=5, choices=status, blank=True)
    task4 = models.CharField(max_length=200, blank=True)
    task4_status = models.CharField(max_length=5, choices=status, blank=True)
    task5 = models.CharField(max_length=200, blank=True)
    task5_status = models.CharField(max_length=5, choices=status, blank=True)
    signed_off = models.BooleanField(blank=False, default=False)
    paid = models.BooleanField(blank=False, default=False)
    project_status = models.CharField(max_length=5, choices=status, blank=False)
    
    def __unicode__(self):
        return self.project_title
    
    def __str__(self):
        return self.project_title

    def get_absolute_url(self):
        return reverse('project_detail', pk={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        
        """ Calculates the VAT charge based on project cost """
        self.plus_vat = self.fee / 5
        
        """ Updates the project status based on the status of other fields """
        if self.signed_off == True:
            self.project_status = 'Done'
        elif self.task1_status != 'To Do':
            self.project_status = 'Doing'
        else:
            self.project_status = 'To Do'
        
        """ Ensures task status fields are filled when corresponding task field is used """
        if self.task2 != '' and self.task2_status == '':
            self.task2_status = 'To Do'
        if self.task3 != '' and self.task3_status == '':
            self.task3_status = 'To Do'
        if self.task4 != '' and self.task4_status == '':
            self.task4_status = 'To Do'
        if self.task5 != '' and self.task5_status == '':
            self.task5_status = 'To Do'
        
        super(Project, self).save(*args, **kwargs)
    
    """ Logic within the save function has been replicated below to be called upon in tests.py """
    
    def seven_days_advance(self):
        now = timezone.now()
        return now + datetime.timedelta(days=7) <= self.deadline
    
    def calculate_vat(self):
        return self.fee / 5
    
    def decide_project_status(self):
        if self.signed_off == True:
            self.project_status = 'Done'
        elif self.task1_status != 'To Do':
            self.project_status = 'Doing'
        else:
            self.project_status = 'To Do'
        return self.project_status
    
    def update_task_status(self):
        if self.task2 != '' and self.task2_status == '':
            self.task2_status = 'To Do'
        return self.task2_status