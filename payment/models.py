from django.db import models
from dashboard.models import Project
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    company_name = models.CharField(max_length=50, blank=False)
    date = models.DateField(blank=False, default=timezone.now)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=True)
    county = models.CharField(max_length=40, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=False)
    
    def __str__(self):
        return "{0}-{1}".format(self.pk, self.date)

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False)
    project = models.ForeignKey(Project, null=False)
    
    def __str__(self):
        return "{0}-{1}".format(self.project.project_title, self.project.fee)