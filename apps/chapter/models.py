import logging

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel

from apps.author.models import Author
from apps.book.models import Book
from apps.category.models import Category

logger = logging.getLogger(__name__)


def get_chapter_audio_upload_path(instance, filename):
    # Use the ISBN of the related book for the audio file's upload path
    return f'audiobooks/{instance.book.isbn}/chapters/{filename}'


class Chapter(TimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    number = models.PositiveIntegerField()  # Chapter number
    title = models.CharField(max_length=255)
    audio_url = models.URLField(null=True, blank=True)
    audio = models.FileField(upload_to=get_chapter_audio_upload_path)
    duration = models.PositiveIntegerField(  # Duration of the chapter in seconds
        validators=[MinValueValidator(1)],
        help_text="Duration of the chapter in seconds."
    )

    def __str__(self):
        return f'Chapter {self.number}: {self.title} ({self.duration} seconds)'


# Pre-save signal for uploading files
@receiver(post_save, sender=Chapter)
def upload_audio(sender, instance, **kwargs):
    try:
        from .tasks import upload_files_to_firebase

        if instance.audio and not instance.audio_url or any(
                error in instance.audio_url for error in ["TimeoutError", "409 PATCH", "Read timed out"]):
            upload_files_to_firebase.delay(file_field=instance.audio.path, file_type='audio', isbn=instance.book.isbn,
                                           folder='audiobooks', subfolder=f'audios/{instance.book.title}',
                                           chapter_pk=instance.number)  # Pass the chapter ID
    except ImportError as e:
        logger.error(f"Failed to import tasks module: {e}")
    except Exception as e:
        logger.error(f"Error during pre-save signal for audio of book {instance.book.title}: {str(e)}")
