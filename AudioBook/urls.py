"""
URL configuration for AudioBook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from AudioBook.settings import local

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

api_urls = [
    path('notification/', include('apps.notification.urls')),
    path('categories/', include('apps.category.urls')),
    path('books/', include('apps.book.urls')),
    path('authors/', include('apps.author.urls')),
    path('chapters/', include('apps.chapter.urls')),
    path('bookmarks/', include('apps.bookmark.urls')),
]

spectacular_urls = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += api_urls
urlpatterns += spectacular_urls

urlpatterns += static(local.MEDIA_URL, document_root=local.MEDIA_ROOT)
urlpatterns += static(local.STATIC_URL, document_root=local.STATIC_ROOT)
