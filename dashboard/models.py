from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Project(models.Model):
    """ Model for individual project plans """
    urgency = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
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
    deadline = models.DateField(blank=True)
    priority = models.CharField(max_length=6, choices=urgency, blank=False)
    task1 = models.CharField(max_length=200, blank=True)
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
        """ Updates the project status based on the status of other fields """
        self.plus_vat = self.fee / 5
        if self.signed_off == True:
            self.project_status = 'Done'
        elif self.task1_status != 'To Do':
            self.project_status = 'Doing'
        else:
            self.project_status = 'To Do'
        super(Project, self).save(*args, **kwargs)