from django.db import models

# Create your models here.


class Uploads(models.Model):
    original_name = models.CharField(max_length=300)
    content_type = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)
    path = models.CharField(max_length=500)
    code = models.CharField(max_length=70, unique=True)
    size = models.IntegerField()

    def __str__(self):
        return self.original_name

    class Meta:
        db_table = 'uploads'
