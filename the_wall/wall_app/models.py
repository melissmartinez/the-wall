from django.db import models
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['fname'])<2:
            errors['fname'] = "Name is too short"
        if len(data['lname'])<2:
            errors['lname'] = "Name is too short"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email is invalid"
        if len(data['password'])<8:
            errors['password']= "Password needs to be 8 characters or longer"
        if data['password']!=data['cpassword']:
            errors['password'] = "Passwords do not match"
        return errors

class MessageManager(models.Manager):
    def validator(self, data):
        errors={}
        if data['message']=="":
            errors['message']="Cannot be empty"
        return errors

class CommentManager(models.Manager):
    def validator(self, data):
        errors={}
        if data['comment']=="":
            errors['comment']="Cannot be empty"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    text = models.TextField()
    user_related = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_messaged")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_related = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_commented")
    message_related = models.ForeignKey('Message',on_delete=models.CASCADE, related_name="message_comented")
    objects = CommentManager()