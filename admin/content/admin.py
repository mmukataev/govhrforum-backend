import csv
from django.http import HttpResponse
from openpyxl import Workbook

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
    list_display = (
        "full_name", "full_position", "country",
        "email", "phone", "session_verbose", "foresight_topics", "iin"
    )
    readonly_fields = ("iin",)
    actions = ["export_as_excel"]

    def full_name(self, obj):
        return f"{obj.surname} {obj.name}"
    full_name.short_description = "ФИО"

    def full_position(self, obj):
        return f"{obj.organization} {obj.position}"
    full_position.short_description = "Должность"

    def session_verbose(self, obj):
        return obj.get_session_display()
    session_verbose.short_description = "Сессия"

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
        return False    # Отключаем изменение

    def has_delete_permission(self, request, obj=None):
        return False 

    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=registrations.xlsx'

        wb = Workbook()
        ws = wb.active
        ws.title = "Регистрации"

        # Заголовки
        ws.append([
            "ФИО", "Должность", "Страна",
            "Email", "Телефон", "Сессия", "Темы", "ИИН"
        ])

        for obj in queryset:
            # Подготовка данных
            full_name = f"{obj.surname} {obj.name}"
            full_position = f"{obj.organization} {obj.position}"
            session = obj.get_session_display() if hasattr(obj, "get_session_display") else obj.session
            topics = (
                ", ".join(obj.foresight_topics.get('Foresight topics'))
                if isinstance(obj.foresight_topics, dict) and isinstance(obj.foresight_topics.get('Foresight topics'), list)
                else str(obj.foresight_topics)
            )

            ws.append([
                full_name,
                full_position,
                obj.country,
                obj.email,
                obj.phone,
                session,
                topics,
                obj.iin,
            ])

        wb.save(response)
        return response


    export_as_excel.short_description = "Экспортировать в Excel"