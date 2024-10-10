from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from apps.book.models import Book
from apps.user.models import UserCategory, UserBook

User = get_user_model()


class CustomUserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'username', 'email', 'phone', 'birth_date', 'image']


class CustomUserCreateSerializer(UserCreateSerializer, CustomUserBaseSerializer):
    class Meta(CustomUserBaseSerializer.Meta, UserCreateSerializer.Meta):
        fields = ['email', 'password', 'birth_date']


class CustomUserSerializer(UserSerializer, CustomUserBaseSerializer):
    class Meta(CustomUserBaseSerializer.Meta, UserSerializer.Meta):
        fields = CustomUserBaseSerializer.Meta.fields


class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ['id', 'category']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book  # Make sure the Book model is correctly imported
        fields = ['id', 'title', 'author_name', 'poster_url']


class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = UserBook
        fields = ['id', 'book']
