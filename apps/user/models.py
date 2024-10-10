from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.book.models import Book
from apps.category.models import Category
from apps.user.validators import validate_image


class CustomUserManager(BaseUserManager):
    def create_user(self, email, birth_date, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not birth_date:
            raise ValueError('The Birth Date field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, birth_date=birth_date, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, birth_date, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, birth_date, password, **extra_fields)


class User(AbstractUser):
    password = models.CharField(max_length=128, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/avatar_default.png',
                              validators=[validate_image],
                              help_text='Upload an avatar image. If not provided, a default image will be used.')
    full_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    genres = models.ManyToManyField(Category, related_name='users', blank=True)
    remember_me = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['birth_date']

    def __str__(self):
        return self.email


class UserCategory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f'{self.user.username} - {self.category.name}'


class UserBook(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
