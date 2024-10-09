from rest_framework import viewsets

from apps.author.serializers import AuthorSerializer
from apps.book.models import Author


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
