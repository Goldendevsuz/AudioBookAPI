from django.core.validators import MinValueValidator
from django.db import models

from apps.book.models import Book


class BookPage(models.Model):
    book = models.ForeignKey(Book, related_name='pages', on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Total number of pages in the ebook (must be between 1 and the book's total pages)"
    )
    content = models.TextField()

    class Meta:
        unique_together = ('book', 'page_number')
        ordering = ['page_number']

    def save(self, **kwargs):
        # Ensure page is not None before saving
        if self.page_number is None:
            raise ValueError("Page cannot be None.")
        if self.page_number > self.book.pages_count:
            raise ValueError(f"Page number cannot exceed {self.book.pages_count} pages.")
        super(BookPage, self).save(**kwargs)

    def __str__(self):
        return f"{self.book.title} - Page {self.page_number}"
