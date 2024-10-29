# apps/aiengine/services/module_management.py
from django.conf import settings
from apps.aiengine.models import ModuleConfig, ModuleLog
from django.utils import timezone
from importlib import import_module
from django.core.cache import cache


def activate_module(module_name, user):
    """
    Ativa um módulo específico e atualiza o cache.
    """
    module, created = ModuleConfig.objects.get_or_create(name=module_name)
    module.is_active = True
    module.save()
    log_module_change(module_name, "Ativado", user)

    if module_name not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS.append(module_name)
        reload_modules()
        cache.set(
            "active_modules", get_active_modules(), timeout=60 * 5
        )  # Atualiza o cache


def deactivate_module(module_name, user):
    """
    Desativa um módulo específico e atualiza o cache.
    """
    try:
        module = ModuleConfig.objects.get(name=module_name)
        module.is_active = False
        module.save()
        log_module_change(module_name, "Desativado", user)

        if module_name in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.remove(module_name)
            reload_modules()
            cache.set("active_modules", get_active_modules(), timeout=60 * 5)
    except ModuleConfig.DoesNotExist:
        pass


def reload_modules():
    """
    Recarrega os módulos configurados em INSTALLED_APPS.
    """
    for app in settings.INSTALLED_APPS:
        import_module(app)


def log_module_change(module_name, action, user):
    """
    Registra alterações nos módulos no banco de dados.
    """
    ModuleLog.objects.create(
        module_name=module_name, action=action, user=user, timestamp=timezone.now()
    )


def get_active_modules():
    """
    Retorna uma lista dos módulos ativos.
    """
    active_modules = ModuleConfig.objects.filter(is_active=True).values_list(
        "name", flat=True
    )
    return list(active_modules)
