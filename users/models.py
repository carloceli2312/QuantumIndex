# QuantumIndex/users/models.py

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Level(models.Model):
    level = models.IntegerField()
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return f'Level {self.level}'


class ProfileLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - Level {self.level.level}'
