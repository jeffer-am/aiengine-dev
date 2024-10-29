# apps/aiengine/views.py

from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from web_project import TemplateLayout
from .models import ModuleConfig, ModuleLog, OpenAIConfig
import openai
import docker
from celery.result import AsyncResult
from django.core.cache import cache


class AIEngineBaseView(LoginRequiredMixin, TemplateView):
    """
    Base view para AI Engine, usando TemplateLayout para inicializar o layout_path dinamicamente.
    """

    template_name = ""

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class AIEngineDashboardView(AIEngineBaseView):
    template_name = "aiengine/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Carregar dados de performance reais do cache ou de uma fonte externa
        performance_data = cache.get("performance_data") or [10, 20, 30, 40]
        cache.set("performance_data", performance_data, timeout=300)

        performance_dates = cache.get("performance_dates") or [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
        ]
        context["performance_data"] = performance_data
        context["performance_dates"] = performance_dates
        context["active_modules"] = ModuleConfig.objects.filter(is_active=True)
        return context


class ManageAppsView(AIEngineBaseView):
    template_name = "aiengine/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["models"] = OpenAIConfig.objects.all()
        context["modules"] = ModuleConfig.objects.all()
        return context


class AIEngineLogsView(AIEngineBaseView):
    template_name = "aiengine/logs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logs"] = ModuleLog.objects.all().order_by("-timestamp")
        return context


class ContainerStatusView(AIEngineBaseView):
    template_name = "aiengine/container_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = docker.from_env()
        containers = client.containers.list(all=True)
        context["containers"] = [
            {
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "N/A",
            }
            for container in containers
        ]
        return context


class TaskStatusView(AIEngineBaseView):
    template_name = "aiengine/task_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_ids = cache.get("task_ids", [])
        tasks = [
            {"id": task_id, "status": AsyncResult(task_id).status}
            for task_id in task_ids
        ]
        context["tasks"] = tasks
        return context


class StatusUpdatesView(AIEngineBaseView):
    template_name = "aiengine/status_updates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_updates"] = "Monitorando atualizações em tempo real"
        return context


class AddModelView(View):
    def post(self, request):
        model_name = request.POST.get("model_name")
        model_version = request.POST.get("model_version")
        model_accuracy = request.POST.get("model_accuracy")

        if model_name and model_version and model_accuracy:
            OpenAIConfig.objects.create(
                default_model=model_name,
                # Campos adicionais, se necessários
            )
            return JsonResponse(
                {"status": "success", "message": "Modelo adicionado com sucesso"}
            )

        return JsonResponse(
            {"status": "error", "message": "Dados inválidos para o modelo"}
        )


class APIConfigView(TemplateView):
    template_name = "aiengine/api_config.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["api_key"] = (
            OpenAIConfig.objects.first().api_key
            if OpenAIConfig.objects.exists()
            else ""
        )
        return context

    def post(self, request, *args, **kwargs):
        api_key = request.POST.get("api_key")
        if api_key:
            config, created = OpenAIConfig.objects.get_or_create(id=1)
            config.api_key = api_key
            config.save()
            messages.success(request, "Chave de API salva com sucesso!")
        return self.get(request, *args, **kwargs)


class APITestConnectionView(View):
    def get(self, request):
        config = OpenAIConfig.objects.first()
        if not config or not config.api_key:
            return JsonResponse(
                {"status": "error", "message": "Chave de API não configurada."}
            )

        openai.api_key = config.api_key
        try:
            openai.Model.list()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Conexão bem-sucedida com a API da OpenAI!",
                }
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Erro ao conectar: {str(e)}"}
            )


class APICostCenterView(TemplateView):
    template_name = "aiengine/api_cost_center.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dados do custo; substitua por lógica real se disponível
        context["cost_data"] = {"usage": 1000, "cost": 150.75}
        return context


class APIUsageStatsView(TemplateView):
    template_name = "aiengine/api_usage_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dados de uso; substitua por lógica real se disponível
        context["usage_stats"] = {"requests": 500, "responses": 490}
        return context
