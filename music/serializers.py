from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Album, Song, Artist


# def source_endswith_mp3(value):
#     if not str(value['source']).endswith('.mp3'):
#         raise ValidationError(detail='mp3 bilan tugasin')

class ArtistSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    cover = serializers.URLField()


class AlbumGetSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    cover = serializers.URLField(required=True)
    artist = ArtistSerializers()


class AlbumPostSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    cover = serializers.URLField(required=True)
    artist = serializers.IntegerField()


# class SongGetSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     cover = serializers.URLField(required=True)
#     source = serializers.URLField(required=True)
#     album = AlbumGetSerializers()
#
#     # def save(self):
#     #     s1 = Song.objects.create(
#     #         title=self.validated_data['title'],
#     #         cover=self.validated_data['cover'],
#     #         source=self.validated_data['source'],
#     #         album=self.validated_data['album']
#     #     )
#     #
#     #     return s1
#
#     # def validate_source(self, value):
#     #     if not str(value).endswith('.mp3'):
#     #         raise ValidationError(detail='mp3 bilan tugasin')
#     #     return value
#
#     def validate(self, date):
#         if not str(date['source']).endswith('.mp3'):
#             raise ValidationError(detail='mp3 bilan tugasin')
#
#     def create(self, validated_data):
#         return Song.objects.create(**validated_data)
#
#
# class SongPostSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     cover = serializers.URLField(required=True)
#     source = serializers.URLField(required=True)
#     album = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Song.objects.create(**validated_data)
class SongModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

