from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Song
from .serializers import SongModelSerializers, SearchSongSerializers
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.postgres.search import TrigramSimilarity
from drf_yasg.utils import swagger_auto_schema


# class SongAPIView(APIView):
#     def get(self, request):
#         songs = Song.objects.all()
#         serializers = SongGetSerializers(songs, many=True)
#         return Response(serializers.data)
#
#     def post(self, request):
#         serializer = SongPostSerializers(data=request.data)
#         # if serializer.is_valid():
#         #     # serializer.save()
#         #     return Response(serializer.data, status=201)
#         # return Response(serializer.errors, status=400)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)

class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongModelSerializers
    pagination_class = LimitOffsetPagination

    # #Post
    # def create(self, request, *args, **kwargs):
    #     pass
    #
    # #Get
    # def list(self, request, *args, **kwargs):
    #     pass
    #
    #
    # def retrieve(self, request, *args, **kwargs):
    #     pass
    #
    # def destroy(self, request, *args, **kwargs):
    #     pass
    #
    # def partial_update(self, request, *args, **kwargs):
    #     pass
    # def update(self, request, *args, **kwargs):
    #     return Response({'message': 'Not allowed'}, status=405)
    @action(detail=True, methods=['GET'])
    def listen(self, request, pk=None):
        song = self.get_object()
        with transaction.atomic():
            song.listened += 1
            song.save()
        return Response({'message': 'bajarildi'})

    @action(detail=False, methods=['GET'])
    def top(self, request):
        songs = Song.objects.all().order_by('-listened')[:3]
        serializers = SongModelSerializers(songs, many=True)
        return Response(serializers.data)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, description='Search parametr', type=openapi.TYPE_STRING)],
        tags=['Search'])
    @action(detail=False, methods=['GET'])
    def search(self, request):
        song_list = []
        q = request.query_params.get('q', None)
        if q is None:
            return Response({'message': 'q parametrini berish kerak'}, status=400)
        songs = Song.objects.annotate(similarity=TrigramSimilarity('title', q)).filter(similarity__gt=0.1).order_by(
            '-similarity')
        # for song in songs:
        #     dict1 = {
        #         'title': song.title,
        #         'cover': song.cover,
        #         'source': song.source,
        #         'listened': song.listened,
        #         'similarity': song.similarity
        #     }
        #     song_list.append(dict1)
        serializers = SearchSongSerializers(songs, many=True)
        return Response(serializers.data)
