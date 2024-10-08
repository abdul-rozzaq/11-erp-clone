from django.contrib import admin

from datetime import timedelta, datetime

from .models import User, Day, Course, Group

admin.site.register(Day)
admin.site.register(Course)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
    )

    ordering = ("pk",)

    list_editable = ("role",)

    list_display_links = ("username",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "title",
        "course",
        "teacher",
        "formatted_start_time",
        "formatted_end_time",
    ]

    list_display_links = ("title",)
