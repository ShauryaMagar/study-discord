from django.db import models
from django.contrib.auth.models import User
# whenever we add a row, we create an instance of the Model class that we create.
# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    #id by default start with 1 and increment as data is added one by one
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #null= True means it cannot be blank. blank ensures that on form submit, the value isn't empty
    #participants
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) #takes time stamp when we first create the instance

    class Meta:
        ordering = ['-updated', '-created'] # -updated means order is descending. updated means order is ascending. First order by updated, then by created

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #cascade means delete all related Messages when Room is deleted. Room and Message has one to many
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[0:50]