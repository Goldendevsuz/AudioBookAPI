from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import AudioUploadView

router = DefaultRouter()
router.register(r'', views.ChapterViewSet, basename='chapter')

urlpatterns = [
    # path('upload/', AudioUploadView.as_view(), name='audio-upload'),
]
urlpatterns += router.urls
