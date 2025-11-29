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
    output = pipe(
        text, 
        max_length=MODELS.MAX_TRANSLATION_LENGTH,
        no_repeat_ngram_size=3,
        repetition_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    return output[0]['translation_text']


def analyze_text_emotion(
    translation_pipe: Pipeline,
    emotion_pipe: Pipeline,
    text: str
) -> TextResult:
    """
    Processa texto completo: tradução e classificação de emoção.
    """
    translated = translate_text(translation_pipe, text)
    result = emotion_pipe(translated)[0][0]
    
    return TextResult(
        original=text,
        translated=translated,
        emotion=result['label'],
        confidence=result['score'] * 100
    )