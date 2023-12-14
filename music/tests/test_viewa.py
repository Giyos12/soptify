from django.test import TestCase, Client
from music.models import Artist, Album, Song
from music.serializers import ArtistSerializers, SongModelSerializers, AlbumGetSerializers

class TestSongViewSet(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name='test artist', cover='https://www.google.com')
        self.album = Album.objects.create(title='test album', artist=self.artist, cover='https://www.google.com')
        self.song = Song.objects.create(title='test song', album=self.album, source='https://www.google.com',
                                        cover='https://www.google.com')
        self.client = Client()

    def test_search(self):
        response = self.client.get('/api/v1/music/song/search/?q=test song')
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        print(response.data)
        self.assertEqual(response.data[0]['title'], 'test song')
        self.assertEqual(len(response.data), 1)

    def test_get_song(self):
        response = self.client.get('/api/v1/music/song/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], 'test song')
        self.assertEqual(len(response.data), 1)

    def test_post_song_serializer(self):
        data = {
            'title': 'test song',
            'album': self.album.id,
            'source': 'https://www.google.com/music.mp3',
            'cover': 'https://www.google.com',
            'listened': 0
        }
        response = self.client.post('/api/v1/music/song/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'test song')
        self.assertEqual(response.data['album'], self.album.id)
        self.assertEqual(response.data['source'], 'https://www.google.com/music.mp3')
        self.assertEqual(response.data['cover'], 'https://www.google.com')
        self.assertEqual(response.data['listened'], 0)

    def test_post_song_serializer_not_valid(self):
        data1 = {
            'source': 'https://www.google.com/music.mp3',
            'cover': 'https://www.google.com',
            'listened': 0
        }
        response = self.client.post('/api/v1/music/song/', data=data1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['title'][0], 'This field is required.')

    # def test_change_song_serializer(self):
    #     data = {
    #         'title': 'test song',
    #         'album': self.album.id,
    #         'source': 'https://www.google.com/music.mp3',
    #         'cover': 'https://www.google.com',
    #         'listened': 0
    #     }
    #     response = self.client.put('/api/v1/music/song/1/', data=data)
    #     self.assertEqual(response.status_code, 415)
    #     self.assertEqual(response.data['title'], 'test song')
    #     self.assertEqual(response.data['album'], self.album.id)
    #     self.assertEqual(response.data['source'], 'https://www.google.com/music.mp3')
    #     self.assertEqual(response.data['cover'], 'https://www.google.com')
    #     self.assertEqual(response.data['listened'], 0)