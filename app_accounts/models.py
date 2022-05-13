from django.contrib.auth.models import User
from django.db import models

from app_uploads.models import Uploads
from django_countries.fields import CountryField


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=15, null=False)
    # profile_image = models.OneToOneField(Uploads, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile',
                                      default='organization/ddede.jpg')
    country = CountryField(multiple=False, null=True)
    address = models.CharField(max_length=300, null=True)

    @classmethod
    def get_default_pk(cls):
        obj, created = cls.objects.get_or_create(name='No Name')
        return obj.pk

    def __str__(self):
        return self.user.username.title()

    class Meta:
        db_table = 'auth_employee'
