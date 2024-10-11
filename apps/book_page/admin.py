from django.contrib import admin

from apps.base.admin import BaseAdmin
from apps.book_page.models import BookPage


class BookPageAdmin(BaseAdmin):
    list_display = ['id', 'short_title', 'page_number', 'short_content']  # Include the custom method in list_display
    list_filter = ['book']

    def short_title(self, obj):
        return obj.book.title[:30] + '...' if len(obj.book.title) > 30 else obj.book

    def short_content(self, obj):
        return obj.content[:30] + '...' if len(
            obj.content) > 30 else obj.content  # Return the first 30 characters of content

    short_title.short_description = 'Book'
    short_content.short_description = 'Content'


admin.site.register(BookPage, BookPageAdmin)
