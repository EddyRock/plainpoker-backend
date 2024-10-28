from django.db import models
from django.contrib.auth.models import User

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    vote = models.IntegerField(null = False)

class Story(models.Model):
    name = models.CharField(max_length = 100, null = True, blank = True)
    votes = models.ManyToManyField(Vote, related_name = 'story_votes')

class Room(models.Model):
    title = models.CharField(max_length = 50, null = True, blank = True)
    stories = models.ManyToManyField(Story, related_name = 'room_stories')
    step = models.IntegerField(null = False)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    users = models.ManyToManyField(User, related_name = 'rooms')
    is_over = models.BooleanField(default = False)