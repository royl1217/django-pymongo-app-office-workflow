from django.contrib import admin
from .models import Employee, AppUser, WorkflowRequest

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
  list_display = ("id", "name")
  search_fields = ("name",)

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
  list_display = ("id", "username", "employee")
  search_fields = ("username",)

@admin.register(WorkflowRequest)
class WorkflowRequestAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "requester", "status", "created_at")
  list_filter = ("status", "created_at")
  search_fields = ("title", "description")