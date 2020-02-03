from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    btitle = models.CharField(max_length=20)
    bauthor = models.CharField(max_length=20)
    bdescription = models.TextField(max_length=100)
    owners = models.ManyToManyField(User)

    def __str__(self):
        return self.btitle

    class Meta:
        db_table = "books"

