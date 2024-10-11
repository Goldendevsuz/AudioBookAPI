from django.contrib import admin

from apps.review.models import Review
from apps.base.admin import BaseAdmin


class ReviewAdmin(BaseAdmin):
    list_display = [f.name for f in Review._meta.fields]


admin.site.register(Review, ReviewAdmin)
