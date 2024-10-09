from django.contrib import admin

from apps.base.admin import BaseAdmin
from apps.chapter.models import Chapter


class ChapterAdmin(BaseAdmin):
    list_display = [f.name for f in Chapter._meta.fields]
    save_as = True


admin.site.register(Chapter, ChapterAdmin)
