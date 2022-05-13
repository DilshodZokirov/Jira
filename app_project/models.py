from django.contrib.auth.models import Group
from django.db import models

# Create your models here.
from django.urls import reverse

from Jira.models import Auditable
from app_accounts.models import Employee
from app_organization.models import Organization, OrgMembers
from app_uploads.models import Uploads


class Project(Auditable):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # slug = models.SlugField()
    image = models.ForeignKey(Uploads, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.title


class ProjectMember(Auditable):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    add = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user.username

    class Meta:
        db_table = 'project_members'
