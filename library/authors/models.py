from django.db import models
from uuid import uuid4
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birthday_year = models.PositiveIntegerField()


class Biography(models.Model):
    text = models.TextField()
    author = models.OneToOneField(Author, on_delete=models.CASCADE)


class Book(models.Model):
    name = models.CharField(max_length=64)
    author = models.ManyToManyField(Author)


class Article(models.Model):

    name = models.CharField(max_length=64)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


# class Users(AbstractBaseUser):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     first_name = models.CharField(max_length=64)
#     last_name = models.CharField(max_length=64)
#     email = models.CharField(
#         max_length=256,
#         unique=True,
#         error_messages={
#             "unique": "A user with that email address already exists.",
#         },
#     )


class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=64)
