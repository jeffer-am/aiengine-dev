# apps/aiengine/services/prepare_finetuning_data.py
import json
from apps.aiengine.models import ModuleLog


def prepare_finetuning_data():
    """
    Prepara um dataset de fine-tuning para OpenAI com base nos logs.
    """
    dataset = []

    logs = ModuleLog.objects.all()[:20]
    for log in logs:
        prompt = f"Log: {log.message}. Action needed."
        completion = generate_completion_based_on_log(log)
        dataset.append({"prompt": prompt, "completion": completion})

    with open("aiengine_finetuning_dataset.jsonl", "w") as f:
        for item in dataset:
            json.dump(item, f)
            f.write("\n")


def generate_completion_based_on_log(log):
    """
    Gera uma resposta ou ação sugerida com base em um log específico.
    """
    if "error" in log.message.lower():
        return "Investigate and resolve the error."
    return "Log reviewed and noted."
