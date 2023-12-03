from django.contrib import admin
from .models import Song, Album, Artist

# Register your models here.

admin.site.register([Album, Artist, Song])

