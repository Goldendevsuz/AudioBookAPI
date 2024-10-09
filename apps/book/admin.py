from django.contrib import admin

from apps.base.admin import BaseAdmin
from apps.book.models import Book


class BookAdmin(BaseAdmin):
    # list_display = [f.name for f in Book._meta.fields]
    list_display = ['id', 'title', 'author', 'rate']
    save_as = True


admin.site.register(Book, BookAdmin)
