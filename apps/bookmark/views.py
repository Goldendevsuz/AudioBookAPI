from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from .models import EbookBookmark, AudiobookBookmark, Book
from .serializers import EbookBookmarkSerializer, AudiobookBookmarkSerializer


class BaseBookmarkViewSet(viewsets.ModelViewSet):
    """
    A base class for Ebook and Audiobook bookmark viewsets.
    Includes common validation logic for checking page or chapter ranges.
    """
    permission_classes = [permissions.IsAdminUser]

    def validate_bookmark(self, book, page_or_chapter, max_range):
        """Common validation logic for checking the page or chapter range."""
        if max_range and (page_or_chapter < 1 or page_or_chapter > max_range):
            raise ValidationError(f"The value must be between 1 and {max_range}.")

    def perform_create(self, serializer):
        book = serializer.validated_data.get('book')
        page_or_chapter = self.get_page_or_chapter(serializer)

        self.validate_bookmark(book, page_or_chapter, self.get_max_range(book))
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        book = serializer.validated_data.get('book')
        page_or_chapter = self.get_page_or_chapter(serializer)

        self.validate_bookmark(book, page_or_chapter, self.get_max_range(book))
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        page_or_chapter = request.data.get(self.page_or_chapter_field())

        if book_id:
            book_instance = Book.objects.get(id=book_id)
            max_range = self.get_max_range(book_instance)

            if book_instance and (int(page_or_chapter) < 1 or int(page_or_chapter) > max_range):
                raise ValidationError(f"The value must be between 1 and {max_range}.")

        return super().partial_update(request, *args, **kwargs)

    def get_max_range(self, book):
        """This method should be overridden by child classes to provide specific logic."""
        raise NotImplementedError("Child classes must implement `get_max_range` method.")

    def get_page_or_chapter(self, serializer):
        """This method should be overridden by child classes to return page or chapter field."""
        raise NotImplementedError("Child classes must implement `get_page_or_chapter` method.")

    def page_or_chapter_field(self):
        """Override this method in child classes to specify if it's 'page' or 'chapter'."""
        raise NotImplementedError("Child classes must implement `page_or_chapter_field` method.")


class EbookBookmarkViewSet(BaseBookmarkViewSet):
    queryset = EbookBookmark.objects.all()
    serializer_class = EbookBookmarkSerializer

    def get_max_range(self, book):
        return book.pages_count  # The maximum value for an ebook is the number of pages

    def get_page_or_chapter(self, serializer):
        return serializer.validated_data.get('page')

    def page_or_chapter_field(self):
        return 'page'

    def get_queryset(self):
        # Return only bookmarks of the current user
        return EbookBookmark.objects.filter(user=self.request.user)


class AudiobookBookmarkViewSet(BaseBookmarkViewSet):
    queryset = AudiobookBookmark.objects.all()
    serializer_class = AudiobookBookmarkSerializer

    def get_max_range(self, book):
        return book.audiobook_chapter_count  # The maximum value for an audiobook is the number of chapters

    def get_page_or_chapter(self, serializer):
        return serializer.validated_data.get('chapter')

    def page_or_chapter_field(self):
        return 'chapter'

    def get_queryset(self):
        # Return only bookmarks of the current user
        return AudiobookBookmark.objects.filter(user=self.request.user)
