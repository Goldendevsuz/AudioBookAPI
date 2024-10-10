import os

from celery import shared_task

from apps.base.firebase_storage import upload_to_firebase
from .models import Book, Chapter


@shared_task(bind=True)
def upload_files_to_firebase(self, file_field, file_type, isbn, folder='audios', subfolder=None, chapter_pk=None):
    try:
        book = Book.objects.get(isbn=isbn)
        chapter = Chapter.objects.get(pk=chapter_pk)  # Now chapter_pk is valid and exists
        file_name = os.path.basename(file_field)

        if file_type == 'audio':
            chapter.audio_url = upload_to_firebase(file_field, file_name, folder=folder, subfolder=subfolder)

        chapter.save()

        # Return the URL or a success message
        return f"Uploaded {file_type} for Book {book.title}: {chapter.audio_url}"

    except Book.DoesNotExist:
        self.update_state(state='FAILURE', meta={'error': 'Book not found'})
        return None
    except Chapter.DoesNotExist:
        self.update_state(state='FAILURE', meta={'error': 'Chapter not found'})
        return None
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        return None
