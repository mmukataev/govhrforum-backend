from django.contrib import admin
from django.utils.html import format_html
from .models import Speaker, News, Registration

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name_en", "role", "photo_preview")
    list_filter = ("role",)
    search_fields = ("name_en", "name_ru", "name_kz")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:5px;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = "Photo"

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title_en", "url_preview", "img_preview")
    search_fields = ("title_kz", "title_ru", "title_en", "description_kz", "description_ru", "description_en")

    def url_preview(self, obj):
        return format_html('<a href="{}" target="_blank" style="color:blue;">{}</a>', obj.url_en, obj.url_en)
    url_preview.short_description = "URL"

    def img_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:5px;" />', obj.img.url)
        return "-"
    img_preview.short_description = "Image"

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    # Указываем, какие поля будут только для чтения
    list_display = ("name", "surname", "organization", "position", "country", "email", "phone", "session", "consent")
    readonly_fields = ("name", "surname", "patronymic", "organization", "position", "country", "email", "phone", "session", "consent", "foresight_topics")

    # Убираем действия "Add", "Delete"
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('auth.add_registration'):
            if 'add' in actions:
                del actions['add']
        if not request.user.has_perm('auth.delete_registration'):
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    # Убираем возможность редактировать или добавлять записи
    def has_add_permission(self, request):
        return False  # Отключаем добавление

    def has_change_permission(self, request, obj=None):
        return False  # Отключаем изменение

    def has_delete_permission(self, request, obj=None):
        return False  # Отключаем удаление