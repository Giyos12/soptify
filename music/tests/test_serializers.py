from django.test import TestCase, Client
from music.models import Artist, Album, Song
from music.serializers import ArtistSerializers, AlbumGetSerializers, SongModelSerializers


class TestSongSerializer(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name='test artist', cover='https://www.google.com')
        self.album = Album.objects.create(title='test album', artist=self.artist, cover='https://www.google.com')
        self.song = Song.objects.create(title='test song', album=self.album, source='https://www.google.com',
                                        cover='https://www.google.com')
        self.song_serializer = SongModelSerializers(instance=self.song)

    def test_contains_expected_fields(self):
        data = self.song_serializer.data
        print(data)
        self.assertEqual(set(data.keys()), set(['id', 'title', 'album', 'cover', 'source', 'listened']))

    def test_data_content(self):
        data = self.song_serializer.data
        self.assertEqual(data['title'], 'test song')

    def test_is_valid_data(self):
        data = {
            'title': 'test song',
            'album': self.album.id,
            'source': 'https://www.google.com/music.mp3',
            'cover': 'https://www.google.com',
            'listened': 0
        }
        song_serializer = SongModelSerializers(data=data)
        self.assertTrue(song_serializer.is_valid())

    def test_is_not_valid_data(self):
        data = {
            'title': 'test song',
            'album': self.album.id,
            'source': 'https://www.google.com/',
            'cover': 'https://www.google.com',
            'listened': 0
        }
        song_serializer = SongModelSerializers(data=data)
        self.assertFalse(song_serializer.is_valid())