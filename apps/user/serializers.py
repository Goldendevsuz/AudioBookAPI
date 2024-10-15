from datetime import timedelta

from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import UserCreateSerializer, UserSerializer, TokenCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from apps.book.models import Book
from apps.user.models import UserCategory, UserBook

User = get_user_model()

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

class CustomTokenCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate user based on email and password
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        # Ensure that the user is not AnonymousUser and is properly authenticated
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication failed")

        refresh = RefreshToken.for_user(user)
        remember_me = attrs.get('remember_me')

        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))
        else:
            refresh.set_exp(lifetime=timedelta(days=7))

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'remember_me': remember_me
        }

        return data