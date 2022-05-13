from django.contrib.auth.models import User, Group
from django.db import models

from Jira.models import Auditable
from app_accounts.models import Employee
from app_uploads.models import Uploads


class Organization(Auditable):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    # image = models.ForeignKey(Uploads, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='organization', blank=True, null=True)
    add = models.BooleanField(default=False)

    class Meta:
        db_table = 'organization'

    def __str__(self):
        return self.title


class OrgMembers(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, default=6)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    add = models.BooleanField(default=False)

    class Meta:
        db_table = 'organization_and_members'

    def __str__(self):
        return f"Organization id {self.org.title} == User id {self.user.user.username}"
