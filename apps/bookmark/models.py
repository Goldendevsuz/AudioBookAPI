from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.book.models import Book

User = get_user_model()


class AbstractBookmark(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_bookmarks")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="%(class)s_bookmarks")

    class Meta:
        abstract = True
        ordering = ['-created']

    def __str__(self):
        return f'{self.user} - {self.book.title} - {self.created}'


class EbookBookmark(AbstractBookmark):
    page = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Total number of pages in the ebook (must be between 1 and the book's total pages)"
    )

    def save(self, **kwargs):
        # Ensure page is not None before saving
        if self.page is None:
            raise ValueError("Page cannot be None.")
        if self.page > self.book.pages_count:
            raise ValueError(f"Page number cannot exceed {self.book.pages_count} pages.")
        super(EbookBookmark, self).save(**kwargs)

    def __str__(self):
        return f'{self.book.title} - Page {self.page}'


class AudiobookBookmark(AbstractBookmark):
    chapter = models.PositiveIntegerField()  # Chapter in the audiobook
    position = models.PositiveIntegerField(  # Time position within the chapter in seconds
        validators=[MinValueValidator(1)],
        help_text="Position in the chapter in seconds."
    )

    def clean(self):
        # Ensure the book has chapters available
        book_chapters = self.book.chapters.all()
        if not book_chapters:
            raise ValidationError(f"The book '{self.book.title}' has no available chapters.")

        # Ensure the specified chapter exists
        chapter_obj = self.book.chapters.filter(number=self.chapter).first()
        if chapter_obj is None:
            raise ValidationError(f"Chapter {self.chapter} does not exist in the book '{self.book.title}'.")

        # Ensure the position is within the chapter's duration
        if self.position > chapter_obj.duration:
            raise ValidationError(
                f"Position {self.position} exceeds the duration of Chapter {self.chapter}, which is {chapter_obj.duration} seconds."
            )

    def save(self, **kwargs):
        # Ensure clean validation is called
        self.clean()
        super().save(**kwargs)

    def __str__(self):
        return f'{self.book.title} - Chapter {self.chapter}, Position {self.position}'
