# apps/aiengine/services/ai_assistant.py
from apps.aiengine.models import OpenAIConfig
import openai


def configure_openai():
    """
    Configura a chave e o modelo padrão para a API da OpenAI.
    """
    config = OpenAIConfig.objects.first()
    if config:
        openai.api_key = config.get_api_key()
        return config.default_model
    else:
        raise Exception("Configuração OpenAI não encontrada.")


def suggest_action_based_on_logs(logs, use_finetuned=True):
    """
    Gera sugestões para ações com base nos logs fornecidos.
    """
    model = "aiengine-finetuned-model" if use_finetuned else configure_openai()
    prompt = generate_dynamic_prompt(logs)
    response = openai.Completion.create(
        engine=model, prompt=prompt, max_tokens=150, temperature=0.7
    )
    return response.choices[0].text.strip()


def generate_dynamic_prompt(logs):
    """
    Gera um prompt dinâmico para a análise de logs.
    """
    log_summary = "\n".join(log.message for log in logs[:5])
    dynamic_prompt = f"Analyze these logs and optimize the system:\n{log_summary}\nSuggest next steps."
    return dynamic_prompt
