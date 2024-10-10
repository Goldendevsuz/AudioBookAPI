from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views
from .views import ShareAudioView

router = DefaultRouter()
router.register(r'', views.ChapterViewSet, basename='chapter')

urlpatterns = [
    path('share-audio/<int:pk>/', ShareAudioView.as_view(), name='share-audio'),
    # path('upload/', AudioUploadView.as_view(), name='audio-upload'),
]
urlpatterns += router.urls
