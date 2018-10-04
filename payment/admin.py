from django.contrib import admin
from dashboard.models import Project
from .models import Order, OrderLineItem

# Register your models here.

class OrderLineAdminInLine(admin.TabularInline):
    model = OrderLineItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInLine, )

admin.site.register(Order, OrderAdmin)