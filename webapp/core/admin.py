from django.contrib import admin
from .models import User, Activity


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "telegram_id",
        "first_name",
        "last_name",
        "birth_date",
        "language",
        "created_at"
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "telegram_id",
        "action",
        "created_at"
    )