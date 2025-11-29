"""Configurações centralizadas da aplicação."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ModelConfig:
    """Configuração dos modelos de IA."""
    TRANSLATION_MODEL: str = "unicamp-dl/translation-pt-en-t5"
    TEXT_EMOTION_MODEL: str = "SamLowe/roberta-base-go_emotions"
    FACIAL_EMOTION_MODEL: str = "dima806/facial_emotions_image_detection"
    MAX_TRANSLATION_LENGTH: int = 400


@dataclass(frozen=True)
class UIConfig:
    """Configuração da interface do usuário."""
    PAGE_TITLE: str = "Classificador de Emoções"
    APP_TITLE: str = "Classificador de Emoções (IA)"
    APP_DESCRIPTION: str = "Insira o Texto e/ou carregue uma Imagem para análise de emoções."
    SUPPORTED_IMAGE_TYPES: tuple = ('png', 'jpg', 'jpeg', 'webp')


@dataclass(frozen=True)
class Messages:
    """Mensagens da aplicação."""
    LOADING_MODELS: str = "Carregando modelos de IA..."
    TRANSLATING: str = "Traduzindo e classificando texto..."
    ANALYZING_IMAGE: str = "Analisando emoções na imagem..."
    NO_INPUT_ERROR: str = "Por favor, insira texto ou carregue uma imagem para iniciar a análise."
    NO_TEXT_WARNING: str = "Nenhum texto foi inserido para análise."
    NO_IMAGE_WARNING: str = "Nenhuma imagem foi carregada para análise."
    COMBINED_WARNING: str = "Insira texto E imagem para ver o resultado combinado."


MODELS = ModelConfig()
UI = UIConfig()
MESSAGES = Messages()