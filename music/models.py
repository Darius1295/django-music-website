from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    artist = models.CharField(max_length=250)
    album_name = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_name


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    track_number = models.IntegerField()

    def __str__(self):
        return self.song_title
