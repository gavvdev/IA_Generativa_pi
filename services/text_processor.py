"""Serviço de processamento de texto."""
from dataclasses import dataclass
from typing import Optional
from transformers import Pipeline

from config.settings import MODELS


@dataclass
class TextResult:
    """Resultado da análise de texto."""
    original: str
    translated: str
    emotion: str
    confidence: float


def translate_text(pipe: Pipeline, text: str) -> str:
    """Traduz texto de Português para Inglês."""
    output = pipe(text, max_length=MODELS.MAX_TRANSLATION_LENGTH)
    return output[0]['translation_text']


def analyze_text_emotion(
    translation_pipe: Pipeline,
    emotion_pipe: Pipeline,
    text: str
) -> TextResult:
    """
    Processa texto completo: tradução e classificação de emoção.
    
    Args:
        translation_pipe: Pipeline de tradução.
        emotion_pipe: Pipeline de classificação de emoções.
        text: Texto original em português.
    
    Returns:
        TextResult com os dados da análise.
    """
    translated = translate_text(translation_pipe, text)
    result = emotion_pipe(translated)[0][0]
    
    return TextResult(
        original=text,
        translated=translated,
        emotion=result['label'],
        confidence=result['score'] * 100
    )