# apps/aiengine/tasks.py

from celery import shared_task
from .models import ModuleLog, OpenAIConfig
import openai
import logging

logger = logging.getLogger(__name__)


@shared_task
def log_model_performance():
    """
    Tarefa periódica para registrar o desempenho do modelo.
    Recupera a configuração do modelo atual e armazena informações de desempenho.
    """
    try:
        config = OpenAIConfig.objects.first()
        if not config:
            logger.warning("Nenhuma configuração de OpenAI encontrada.")
            return

        openai.api_key = config.get_api_key()
        response = openai.Model.list()

        # Exemplo fictício de análise de resposta
        performance_data = {
            "model": config.default_model,
            "response_time": len(response["data"])
            * 10,  # Exemplo: tempo fictício de resposta
        }

        # Registro no log para análise posterior
        ModuleLog.objects.create(
            module_name="PerformanceLogger",
            action="Registro de desempenho",
            message=f"Dados de desempenho: {performance_data}",
        )
        logger.info("Desempenho do modelo registrado com sucesso.")

    except Exception as e:
        logger.error(f"Erro ao registrar o desempenho do modelo: {e}")


@shared_task
def clean_old_logs(days=30):
    """
    Limpeza de logs antigos com mais de 'days' dias.
    """
    from django.utils import timezone
    from datetime import timedelta

    threshold_date = timezone.now() - timedelta(days=days)
    old_logs = ModuleLog.objects.filter(timestamp__lt=threshold_date)
    count = old_logs.count()
    old_logs.delete()

    logger.info(f"Limpeza de {count} logs antigos concluída.")
