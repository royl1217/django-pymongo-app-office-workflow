# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.hashers import make_password, check_password


# class Employee(models.Model):
#   name = models.CharField(max_length=200)

#   def __str__(self):
#     return self.name


# class AppUser(models.Model):
#   username = models.CharField(max_length=100, unique=True)
#   password_hash = models.CharField(max_length=255)
#   employee = models.OneToOneField(
#     Employee,
#     on_delete=models.CASCADE,
#     null=True,
#     blank=True,
#     related_name="user_account"
#   )

#   def set_password(self, raw_password):
#     self.password_hash = make_password(raw_password)

#   def check_password(self, raw_password):
#     return check_password(raw_password, self.password_hash)

#   def __str__(self):
#     return self.username


# class WorkflowRequest(models.Model):
#   STATUS_CHOICES = [
#     ("PENDING", "Pending"),
#     ("APPROVED", "Approved"),
#     ("REJECTED", "Rejected"),
#     ("IN_PROGRESS", "In progress"),
#     ("COMPLETED", "Completed"),
#   ]

#   title = models.CharField(max_length=200)
#   description = models.TextField(blank=True)

#   requester = models.ForeignKey(
#     Employee,
#     on_delete=models.CASCADE,
#     related_name="requests"
#   )

#   approver = models.ForeignKey(
#     Employee,
#     on_delete=models.PROTECT,
#     related_name="approvals",
#     null=True,
#     blank=True
#   )

#   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
#   created_at = models.DateTimeField(default=timezone.now)
#   updated_at = models.DateTimeField(auto_now=True)
#   due_date = models.DateField(null=True, blank=True)

#   def __str__(self):
#     return f"{self.title} ({self.status})"

from mongoengine import (
  Document,
  StringField,
  ReferenceField,
  DateTimeField,
  DateField
)
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class Employee(Document):
  name = StringField(required=True, max_length=200)

  def __str__(self):
    return self.name


class AppUser(Document):
  username = StringField(required=True, unique=True, max_length=100)
  password_hash = StringField(required=True)
  employee = ReferenceField(Employee, required=False)

  def set_password(self, raw_password):
    self.password_hash = make_password(raw_password)

  def check_password(self, raw_password):
    return check_password(raw_password, self.password_hash)

  def __str__(self):
    return self.username


class WorkflowRequest(Document):
  STATUS_CHOICES = (
    "PENDING",
    "APPROVED",
    "REJECTED",
    "IN_PROGRESS",
    "COMPLETED",
  )

  title = StringField(required=True, max_length=200)
  description = StringField()
  requester = ReferenceField(Employee, required=True)
  approver = ReferenceField(Employee, required=False)
  status = StringField(choices=STATUS_CHOICES, default="PENDING")
  created_at = DateTimeField(default=timezone.now)
  updated_at = DateTimeField(default=timezone.now)
  due_date = DateField(required=False)

  def __str__(self):
    return f"{self.title} ({self.status})"