from __future__ import unicode_literals
from django.db import models
import re

## MANAGERS

class User_Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        name_regex = re.compile(r'^[a-zA-z]+$')
        if not name_regex.match(postData['first_name']):
            errors['first_name'] = "First name must contain letters only!"
        if not name_regex.match(postData['last_name']):
            errors['first_name'] = "Last name must contain letters only!"
        if len(postData['first_name']) < 2:
            errors['f_name_length'] = "First name must be at least two characters!"
        if len(postData['last_name']) < 2:
            errors['l_name_length'] = "Last name must be at least two characters!"
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address!"
        email_duplicate_check = User.objects.filter(email = postData['email'])
        if email_duplicate_check:
            errors['dupe_email'] = "Email already exists!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least eight characters!"
        if postData['password'] != postData['conf_pw']:
            errors['conf_pw'] = "Password and Confirmation Password Must Match!"
        return errors
    def update(self, postData):
        errors = {}
        name_regex = re.compile(r'^[a-zA-z]+$')
        if not name_regex.match(postData['first_name']):
            errors['first_name'] = "First name must contain letters only!"
        if not name_regex.match(postData['last_name']):
            errors['last_name'] = "Last name must contain letters only!"
        if len(postData['first_name']) < 2:
            errors['f_name_length'] = "First name must be at least two characters!"
        if len(postData['last_name']) < 2:
            errors['l_name_length'] = "Last name must be at least two characters!"
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address!"
        this_user = User.objects.get(id=postData['user_id'])
        if this_user.email != postData['email']:
            email_duplicate_check = User.objects.filter(email = postData['email'])
            if email_duplicate_check:
                errors['dupe_email'] = "Email already exists!"
        return errors

class Quote_Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author name must at least three characters!"
        if len(postData['content']) < 10:
            errors['content'] = "Quote must be at least 10 characters!"
        return errors

## NORMAL CLASSES

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name = 'uploaded_quotes', on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name = 'liked_quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Quote_Manager()
