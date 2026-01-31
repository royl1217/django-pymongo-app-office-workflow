from django.shortcuts import render, redirect, get_object_or_404
from .models import WorkflowRequest, AppUser, Employee
from .forms import WorkflowRequestForm, RegisterForm, LoginForm


# -----------------------------
# Helper: get current logged-in user
# -----------------------------
def get_current_user(request):
  user_id = request.session.get("user_id")
  if not user_id:
    return None
  try:
    return AppUser.objects.get(pk=user_id)
  except AppUser.DoesNotExist:
    return None


# -----------------------------
# Authentication: Register
# -----------------------------
def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = AppUser(username=form.cleaned_data["username"])
      user.set_password(form.cleaned_data["password"])
      user.save()

      employee = Employee.objects.create(
        name=form.cleaned_data["username"]
      )

      user.employee = employee
      user.save()

      request.session["user_id"] = str(user.id)
      return redirect("dashboard")
  else:
    form = RegisterForm()

  return render(request, "workflow/register.html", {"form": form})


# -----------------------------
# Authentication: Login
# -----------------------------
def login_view(request):
  if request.method == "POST":
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data["username"]
      password = form.cleaned_data["password"]

      try:
        user = AppUser.objects.get(username=username)
      except AppUser.DoesNotExist:
        user = None

      if user and user.check_password(password):
        request.session["user_id"] = str(user.id)
        return redirect("dashboard")
      else:
        form.add_error(None, "Invalid username or password")
  else:
    form = LoginForm()

  return render(request, "workflow/login.html", {"form": form})


# -----------------------------
# Authentication: Logout
# -----------------------------
def logout_view(request):
  request.session.flush()
  return redirect("login")


# -----------------------------
# Dashboard
# -----------------------------
def dashboard(request):
  user = get_current_user(request)
  if not user:
    return redirect("login")

  employee = user.employee

  pending = WorkflowRequest.objects.filter(requester=employee, status="PENDING").count()
  approved = WorkflowRequest.objects.filter(requester=employee, status="APPROVED").count()
  rejected = WorkflowRequest.objects.filter(requester=employee, status="REJECTED").count()
  in_progress = WorkflowRequest.objects.filter(requester=employee, status="IN_PROGRESS").count()
  completed = WorkflowRequest.objects.filter(requester=employee, status="COMPLETED").count()

  return render(request, "workflow/dashboard.html", {
    "employee": employee,
    "pending": pending,
    "approved": approved,
    "rejected": rejected,
    "in_progress": in_progress,
    "completed": completed,
  })


# -----------------------------
# List Requests (two sections)
# -----------------------------
def request_list(request):
  user = get_current_user(request)
  if not user:
    return redirect("login")

  employee = user.employee

  # Requests submitted by me
  my_requests = WorkflowRequest.objects.filter(
    requester=employee
  ).order_by("-created_at")

  # Requests waiting for my approval
  to_approve = WorkflowRequest.objects.filter(
    approver=employee,
    status="PENDING"
  ).order_by("-created_at")

  return render(request, "workflow/request_list.html", {
    "employee": employee,
    "my_requests": my_requests,
    "to_approve": to_approve,
  })


# -----------------------------
# Create Request
# -----------------------------
def request_create(request):
  user = get_current_user(request)
  if not user:
    return redirect("login")

  employee = user.employee

  if request.method == "POST":
    form = WorkflowRequestForm(request.POST)
    if form.is_valid():
      obj = form.save(commit=False)
      obj.requester = employee
      obj.save()
      return redirect("request_list")
  else:
    form = WorkflowRequestForm()

  return render(request, "workflow/request_form.html", {
    "form": form,
    "employee": employee,
  })


# -----------------------------
# Request Detail
# -----------------------------
def request_detail(request, pk):
  user = get_current_user(request)
  if not user:
    return redirect("login")

  employee = user.employee

  req = get_object_or_404(WorkflowRequest, pk=pk)

  # requester can view
  # approver can view
  if req.requester != employee and req.approver != employee:
    return redirect("request_list")

  return render(request, "workflow/request_detail.html", {
    "request_obj": req,
    "employee": employee,
  })


# -----------------------------
# Approve Request
# -----------------------------
def request_approve(request, pk):
  user = get_current_user(request)
  if not user:
    return redirect("login")

  employee = user.employee

  req = get_object_or_404(
    WorkflowRequest,
    pk=pk,
    approver=employee
  )

  req.status = "APPROVED"
  req.save()

  return redirect("request_detail", pk=pk)


# -----------------------------
# Reject Request
# -----------------------------
def request_reject(request, pk):
  user = get_current_user(request)
  if not user:
    return redirect("login")

  employee = user.employee

  req = get_object_or_404(
    WorkflowRequest,
    pk=pk,
    approver=employee
  )

  req.status = "REJECTED"
  req.save()

  return redirect("request_detail", pk=pk)