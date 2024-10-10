import os

from celery import shared_task
from icecream import ic
from apps.base.firebase_storage import upload_to_firebase
from .models import Book


@shared_task(bind=True)
def upload_files_to_firebase(self, file_field, file_type, isbn, folder='audiobooks', subfolder=None):
    ic(isbn)
    try:
        # Find the book by ISBN
        book = Book.objects.get(isbn=isbn)
        ic(book)

        # Use the original file name instead of generating a new one
        file_name = os.path.basename(file_field)

        # Upload based on file type
        if file_type == 'poster':
            book.poster_url = upload_to_firebase(file_field, file_name, folder=folder, subfolder=subfolder)
        elif file_type == 'cover':
            book.cover_url = upload_to_firebase(file_field, file_name, folder=folder, subfolder=subfolder)
        elif file_type == 'ebook':
            book.ebook_url = upload_to_firebase(file_field, file_name, folder=folder, subfolder=subfolder)

        # Save the book
        book.save()

        # Return success messages
        messages = []
        if book.poster_url:
            messages.append(f"Uploaded poster for ISBN {isbn}: {book.poster_url}")
        if book.cover_url:
            messages.append(f"Uploaded cover for ISBN {isbn}: {book.cover_url}")
        if book.ebook_url:
            messages.append(f"Uploaded ebook for ISBN {isbn}: {book.ebook_url}")
        return messages

    except Book.DoesNotExist:
        self.update_state(state='FAILURE', meta={'error': 'Book not found'})
        return None
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        return None
