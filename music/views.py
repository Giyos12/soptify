from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Song
from .serializers import SongGetSerializers, SongPostSerializers


class SongAPIView(APIView):
    def get(self, request):
        songs = Song.objects.all()
        serializers = SongGetSerializers(songs, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = SongPostSerializers(data=request.data)
        # if serializer.is_valid():
        #     # serializer.save()
        #     return Response(serializer.data, status=201)
        # return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
