from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    DEPARTMENT_CHOICES = [
        # ('JOURNAL TEAM', 'JOURNAL TEAM'),
        # ('RESEARCH WORK DEVELOPMENT TEAM', 'RESEARCH WORK DEVELOPMENT TEAM'),
        # ('SOFTWARE PROJECT DEVELOPMENT TEAM', 'SOFTWARE PROJECT DEVELOPMENT TEAM'),
        ('HARDWARE PROJECT DEVELOPMENT TEAM', 'HARDWARE PROJECT DEVELOPMENT TEAM'),
        # ('TECHNICAL TEAM', 'TECHNICAL TEAM'),
        ('ADMIN TEAM', 'ADMIN TEAM'),
        ('ADMIN-MANAGEMENT WORK TEAM', 'ADMIN-MANAGEMENT WORK TEAM'),
    ]

    BRANCH_CHOICES = [
        ('NAGERCOIL', 'NAGERCOIL'),
        # ('TIRUNELVELI', 'TIRUNELVELI'),
        # ('CHENNAI', 'CHENNAI'),
        # ('PUDUKOTTAI', 'PUDUKOTTAI'),
        # ('VIJAYAWADA','VIJAYAWADA')
        
    ]
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    is_team_leader = models.BooleanField(default=False) 
    is_approved = models.BooleanField(default=False)  # ✅ New field for admin approval 

    def __str__(self):
        return f"{self.username} - {self.department} - {self.branch} - {'Approved' if self.is_approved else 'Pending'}"

class WorkStatusGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    S_NO=models.CharField(max_length=100)
    DATE = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.DATE}"

class WorkStatus(models.Model):
    group = models.ForeignKey(WorkStatusGroup, on_delete=models.CASCADE, related_name='statuses')
    WORK_CODE = models.CharField(max_length=50)
    WORK_DETAILS = models.TextField()
    STARTING_DATE = models.DateField(null=True, blank=True)
    ENDING_DATE = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('IN PROGRESS', 'IN PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
        ('-', '-')
    ]
    WORK_STATUS = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.WORK_CODE} - {self.WORK_STATUS}"