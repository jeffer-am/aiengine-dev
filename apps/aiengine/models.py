from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.utils import timezone
import os


class OpenAIConfig(models.Model):
    MODEL_CHOICES = [
        ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
        ("gpt-4-mini", "GPT-4 Mini"),
        ("gpt-4", "GPT-4"),
    ]

    default_model = models.CharField(
        max_length=50, choices=MODEL_CHOICES, default="gpt-3.5-turbo"
    )
    api_key_encrypted = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def set_api_key(self, api_key):
        cipher_suite = Fernet(os.environ.get("SECRET_KEY").encode())
        self.api_key_encrypted = cipher_suite.encrypt(api_key.encode())

    def get_api_key(self):
        cipher_suite = Fernet(os.environ.get("SECRET_KEY").encode())
        return cipher_suite.decrypt(self.api_key_encrypted).decode()


class ModuleLog(models.Model):
    module_name = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)


class ModuleConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {'Ativo' if self.is_active else 'Desativado'}"
