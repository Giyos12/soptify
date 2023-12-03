from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=200)
    cover = models.URLField(null=True, blank=True)
    source = models.URLField(null=False)
    album = models.ForeignKey('music.album', on_delete=models.CASCADE, null=True)

    # class Meta:
    #     unique_together = ('title','cover')
