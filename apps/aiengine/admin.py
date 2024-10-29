from django.contrib import admin
from .models import OpenAIConfig, ModuleLog, ModuleConfig
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
import openai


@admin.register(OpenAIConfig)
class OpenAIConfigAdmin(admin.ModelAdmin):
    list_display = ("default_model", "test_connection_button")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:object_id>/test-connection/",
                self.admin_site.admin_view(self.test_connection_view),
                name="openaiconfig-test-connection",
            ),
        ]
        return custom_urls + urls

    def test_connection_button(self, obj):
        return format_html(
            '<a class="btn btn-primary" href="{}">Testar Conexão</a>',
            f"/admin/aiengine/openaiconfig/{obj.id}/test-connection/",
        )

    def test_connection_view(self, request, object_id, *args, **kwargs):
        config = self.get_object(request, object_id)
        if config:
            try:
                openai.api_key = config.get_api_key()
                openai.Model.list()
                messages.success(request, "Conexão com OpenAI bem-sucedida!")
            except Exception as e:
                messages.error(request, f"Falha na conexão: {e}")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@admin.register(ModuleLog)
class ModuleLogAdmin(admin.ModelAdmin):
    list_display = ("module_name", "action", "user", "timestamp")


@admin.register(ModuleConfig)
class ModuleConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
