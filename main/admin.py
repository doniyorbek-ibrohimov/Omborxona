from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomEmployeeAdmin(UserAdmin):
    model = Employee
    list_display = ['username', 'is_admin', 'is_sales', 'is_staff']

admin.site.register(Branch)
admin.site.register(Product)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Record)

