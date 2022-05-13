from django.db import models

# Create your models here.
from django.utils import timezone

from Jira.models import Auditable
from app_accounts.models import Employee
from app_project.models import Project
from app_uploads.models import Uploads


class Task(Auditable):
    title = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
    image = models.ForeignKey(Uploads, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task'


class TaskMember(Auditable):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    add = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user.username

    class Meta:
        db_table = 'task_members'


class Comment(Auditable):
    post = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField()
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'comment'


def approved_comments(self):
    return self.comments.filter(approved_comment=True)
