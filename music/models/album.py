from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=200)
    cover = models.URLField(null=True, blank=True)
    artist = models.ForeignKey('music.Artist', on_delete=models.CASCADE)
