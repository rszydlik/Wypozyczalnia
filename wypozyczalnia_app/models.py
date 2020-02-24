from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    btitle = models.CharField(max_length=20)
    bauthor = models.CharField(max_length=20)
    bdescription = models.TextField(max_length=100)
    owners = models.ManyToManyField(User, through='Library')

    def __str__(self):
        return self.btitle

    class Meta:
        db_table = "books"


class Friend(models.Model):
    name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=16, null=True)
    relates = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Library(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Friend, on_delete=models.CASCADE, null=True)
