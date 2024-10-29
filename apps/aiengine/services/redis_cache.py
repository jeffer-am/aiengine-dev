# apps/aiengine/services/redis_cache.py
from django.core.cache import cache
from apps.aiengine.models import ModuleConfig


def get_active_modules():
    """
    Retorna módulos ativos usando cache Redis para otimização.
    """
    active_modules = cache.get("active_modules")
    if not active_modules:
        active_modules = list(
            ModuleConfig.objects.filter(is_active=True).values_list("name", flat=True)
        )
        cache.set("active_modules", active_modules, timeout=60 * 5)
    return active_modules
