from django.contrib import admin
from .models import Organization, OrgMembers

# Register your models here.
admin.site.register(Organization)
admin.site.register(OrgMembers)
