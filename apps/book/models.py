import logging

from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel

from apps.author.models import Author
from apps.category.models import Category

logger = logging.getLogger(__name__)


class Book(TimeStampedModel):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    rate = models.FloatField(validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])
    categories = models.ManyToManyField(Category, related_name='books')
    summary = models.TextField(max_length=3000, unique=True)
    isbn = models.CharField(max_length=13, unique=True, validators=[MinLengthValidator(13)])

    poster_url = models.URLField(null=True, blank=True)
    cover_url = models.URLField(null=True, blank=True)
    ebook_url = models.URLField(null=True, blank=True)

    poster = models.FileField(upload_to='audiobooks/posters/', null=True, blank=True)
    cover = models.FileField(upload_to='audiobooks/covers/', null=True, blank=True)
    ebook = models.FileField(upload_to='audiobooks/ebooks/', null=True, blank=True)

    def __str__(self):
        return self.title


# Pre-save signal for uploading files
@receiver(pre_save, sender=Book)
def upload_files(sender, instance, **kwargs):
    try:
        from .tasks import upload_files_to_firebase

        if instance.poster and (not instance.poster_url or any(
                error in instance.poster_url for error in ["TimeoutError", "409 PATCH", "Read timed out"])):
            upload_files_to_firebase.delay(file_field=instance.poster.path, file_type='poster', isbn=instance.isbn,
                                           folder='audiobooks', subfolder='posters')

        if instance.cover and not instance.cover_url or any(
                error in instance.cover_url for error in ["TimeoutError", "409 PATCH", "Read timed out"]):
            upload_files_to_firebase.delay(file_field=instance.cover.path, file_type='cover', isbn=instance.isbn,
                                           folder='audiobooks', subfolder='covers')

        if instance.ebook and not instance.ebook_url or any(
                error in instance.ebook_url for error in ["TimeoutError", "409 PATCH", "Read timed out"]):
            upload_files_to_firebase.delay(file_field=instance.ebook.path, file_type='ebook', isbn=instance.isbn,
                                           folder='audiobooks', subfolder='ebooks')

    except ImportError as e:
        logger.error(f"Failed to import tasks module: {e}")
    except Exception as e:
        logger.error(f"Error during pre-save signal for book {instance.isbn}: {str(e)}")
