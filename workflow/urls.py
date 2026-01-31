from django.urls import path
from . import views

app_name = "workflow"

urlpatterns = [
  # Authentication
  path("register/", views.register, name="register"),
  path("login/", views.login_view, name="login"),
  path("logout/", views.logout_view, name="logout"),

  # Dashboard
  path("", views.dashboard, name="dashboard"),

  # Workflow Requests
  path("requests/", views.request_list, name="request_list"),
  path("requests/new/", views.request_create, name="request_create"),
  path("requests/<str:pk>/", views.request_detail, name="request_detail"),

  # Workflow Actions
  path("requests/<str:pk>/approve/", views.request_approve, name="request_approve"),
  path("requests/<str:pk>/reject/", views.request_reject, name="request_reject"),
]