# apps/aiengine/urls.py

from django.urls import path
from .views import (
    AIEngineDashboardView,
    ManageAppsView,
    AIEngineLogsView,
    ContainerStatusView,
    TaskStatusView,
    StatusUpdatesView,
    AddModelView,
    APIConfigView,  # Nova view para configuração da API
    APITestConnectionView,  # Nova view para testar a conexão da API
    APICostCenterView,  # Nova view para o centro de custos
    APIUsageStatsView,  # Nova view para estatísticas de uso
)

urlpatterns = [
    path(
        "dashboard/",
        AIEngineDashboardView.as_view(),
        name="app-aiengine-dashboard",
    ),
    path(
        "manage/",
        ManageAppsView.as_view(),
        name="app-aiengine-manage",
    ),
    path(
        "logs/",
        AIEngineLogsView.as_view(),
        name="app-aiengine-logs",
    ),
    path(
        "container-status/",
        ContainerStatusView.as_view(),
        name="app-aiengine-container-status",
    ),
    path(
        "task-status/",
        TaskStatusView.as_view(),
        name="app-aiengine-task-status",
    ),
    path(
        "status-updates/",
        StatusUpdatesView.as_view(),
        name="app-aiengine-status-updates",
    ),
    path(
        "add-model/",
        AddModelView.as_view(),
        name="app-aiengine-add-model",
    ),
    # Novas rotas para funcionalidades da API
    path(
        "api/config/",
        APIConfigView.as_view(),
        name="app-aiengine-api-config",
    ),
    path(
        "api/test-connection/",
        APITestConnectionView.as_view(),
        name="app-aiengine-api-test",
    ),
    path(
        "api/cost-center/",
        APICostCenterView.as_view(),
        name="app-aiengine-api-cost",
    ),
    path(
        "api/usage-stats/",
        APIUsageStatsView.as_view(),
        name="app-aiengine-usage-stats",
    ),
]
