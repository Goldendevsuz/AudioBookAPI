from django.contrib import admin

from apps.base.admin import BaseAdmin
from apps.bookmark.models import AudiobookBookmark, EbookBookmark


class EbookBookmarkAdmin(BaseAdmin):
    list_display = [f.name for f in EbookBookmark._meta.fields]


class AudiobookBookmarkAdmin(BaseAdmin):
    list_display = [f.name for f in AudiobookBookmark._meta.fields]


admin.site.register(AudiobookBookmark, AudiobookBookmarkAdmin)


# @admin.register(AudiobookBookmark)
class AudiobookBookmarkAdmin(admin.ModelAdmin):
    # This ensures the validation is run when saving from the admin interface
    def save_model(self, request, obj, form, change):
        # The clean method will be called before saving the object
        obj.clean()  # Ensures the model-level validation is applied
        super().save_model(request, obj, form, change)


admin.site.register(EbookBookmark, EbookBookmarkAdmin)
