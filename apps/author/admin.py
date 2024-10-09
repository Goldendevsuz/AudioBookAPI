from django.contrib import admin

from apps.author.models import Author
from apps.base.admin import BaseAdmin


class AuthorAdmin(BaseAdmin):
    list_display = [f.name for f in Author._meta.fields]


admin.site.register(Author, AuthorAdmin)
