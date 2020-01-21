from django.db import models


# Create your models here.
class Book(models.Model):
    btitle = models.CharField(max_length=20)
    bauthor = models.CharField(max_length=20)
    bdescription = models.TextField(max_length=100)

    class Meta:
        db_table = "books"
