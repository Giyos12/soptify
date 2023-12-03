from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    cover = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
