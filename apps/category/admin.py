from django.contrib import admin

from .models import Category
from ..base.admin import BaseAdmin


class Usergenres(BaseAdmin):
    list_display = ('name',)  # Assuming 'name' is a field in Category


admin.site.register(Category, Usergenres)
