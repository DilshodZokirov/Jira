from django.db import modelsfrom app_accounts.models import Userclass Auditable(models.Model):    created_at = models.DateTimeField(auto_now=True)    updated_at = models.DateTimeField(auto_now_add=True)    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="+")    deleted = models.BooleanField(default=False)    class Meta:        abstract = True