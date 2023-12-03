from django.urls import path
from .views import SongAPIView

urlpatterns = [
    path('', SongAPIView.as_view(), name='song')
]
