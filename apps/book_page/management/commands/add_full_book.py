from django.core.management.base import BaseCommand
from apps.book_page.models import BookPage
from apps.book.models import Book
from django.core.exceptions import ObjectDoesNotExist
import pdfplumber
import os


class Command(BaseCommand):
    help = 'Add full book content in pages from a PDF file'

    def add_arguments(self, parser):
        parser.add_argument('isbn', type=str, help='ISBN of the book to add pages for')
        parser.add_argument('file_path', type=str, help='Path to the book PDF file')
        parser.add_argument('--words_per_page', type=int, default=300, help='Number of words per page')

    def handle(self, *args, **kwargs):
        isbn = kwargs['isbn']
        file_path = kwargs['file_path']
        words_per_page = kwargs['words_per_page']

        try:
            book = Book.objects.get(isbn=isbn)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Book with ISBN {isbn} does not exist.'))
            return

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} does not exist.'))
            return

        full_text = ""

        # Extract text from PDF
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"  # Combine text from all pages

        # Split text into words
        words = full_text.split()
        total_words = len(words)
        total_pages = (total_words // words_per_page) + (1 if total_words % words_per_page > 0 else 0)

        # Splitting the full text into pages
        for page_number in range(1, total_pages + 1):
            start = (page_number - 1) * words_per_page
            end = min(start + words_per_page, total_words)  # Ensure end does not exceed total words
            content = ' '.join(words[start:end])

            # Create and save the page
            BookPage.objects.create(book=book, page_number=page_number, content=content)

        self.stdout.write(self.style.SUCCESS(f'Successfully added pages for book "{book.title}".'))
