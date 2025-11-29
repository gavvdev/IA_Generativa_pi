"""Serviço de combinação de resultados usando análise inteligente."""
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from .text_processor import TextResult
from .image_processor import ImageResult


@dataclass
class CombinedAnalysis:
    """Resultado da análise combinada."""
    text_emotion: str
    image_emotion: str
    summary: str
    interpretation: str
    consistency: str


# Mapeamento de emoções para português e categorias
EMOTION_MAP = {
    # Positivas
    "joy": ("Alegria", "positiva"),
    "happy": ("Felicidade", "positiva"),
    "happiness": ("Felicidade", "positiva"),
    "love": ("Amor", "positiva"),
    "admiration": ("Admiração", "positiva"),
    "amusement": ("Diversão", "positiva"),
    "gratitude": ("Gratidão", "positiva"),
    "excitement": ("Empolgação", "positiva"),
    "optimism": ("Otimismo", "positiva"),
    # Negativas
    "sad": ("Tristeza", "negativa"),
    "sadness": ("Tristeza", "negativa"),
    "anger": ("Raiva", "negativa"),
    "angry": ("Raiva", "negativa"),
    "fear": ("Medo", "negativa"),
    "disgust": ("Nojo", "negativa"),
    "disappointment": ("Decepção", "negativa"),
    "annoyance": ("Irritação", "negativa"),
    "grief": ("Luto", "negativa"),
    # Neutras
    "neutral": ("Neutra", "neutra"),
    "surprise": ("Surpresa", "neutra"),
    "curiosity": ("Curiosidade", "neutra"),
    "confusion": ("Confusão", "neutra"),
}


def get_emotion_info(emotion: str) -> tuple:
    """Retorna nome em PT e categoria da emoção."""
    return EMOTION_MAP.get(emotion.lower(), (emotion.capitalize(), "indefinida"))


def generate_interpretation(
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult]
) -> str:
    """Gera interpretação inteligente das emoções."""
    if not text_result or not image_result:
        return "Análise incompleta - necessário texto e imagem."
    
    text_em, text_cat = get_emotion_info(text_result.emotion)
    image_em, image_cat = get_emotion_info(image_result.emotion)
    
    text_conf = text_result.confidence
    image_conf = image_result.confidence
    
    # Mesma emoção
    if text_result.emotion.lower() == image_result.emotion.lower():
        return (
            f"✨ **Emoções consistentes**: Tanto o texto quanto a expressão facial "
            f"indicam **{text_em}**. Isso sugere que a pessoa está expressando "
            f"genuinamente esse sentimento, com alta confiabilidade na análise "
            f"(Texto: {text_conf:.0f}%, Imagem: {image_conf:.0f}%)."
        )
    
    # Mesma categoria (ex: joy/happy)
    if text_cat == image_cat:
        return (
            f"🔄 **Emoções similares**: O texto expressa **{text_em}** ({text_conf:.0f}%) "
            f"enquanto a face demonstra **{image_em}** ({image_conf:.0f}%). "
            f"Ambas são emoções {text_cat}s, indicando coerência no estado emocional geral."
        )
    
    # Categorias diferentes
    if text_cat == "positiva" and image_cat == "negativa":
        return (
            f"⚠️ **Divergência emocional**: O texto sugere **{text_em}** (emoção positiva), "
            f"mas a expressão facial indica **{image_em}** (emoção negativa). "
            f"Isso pode indicar uma tentativa de mascarar sentimentos reais ou "
            f"uma comunicação irônica/sarcástica."
        )
    
    if text_cat == "negativa" and image_cat == "positiva":
        return (
            f"⚠️ **Divergência emocional**: O texto expressa **{text_em}** (emoção negativa), "
            f"enquanto a face mostra **{image_em}** (emoção positiva). "
            f"A pessoa pode estar tentando manter aparências ou o contexto "
            f"do texto não reflete seu estado emocional real."
        )
    
    # Neutro envolvido
    if text_cat == "neutra" or image_cat == "neutra":
        return (
            f"📊 **Análise mista**: O texto indica **{text_em}** ({text_conf:.0f}%) "
            f"e a expressão facial mostra **{image_em}** ({image_conf:.0f}%). "
            f"Uma das análises é neutra, sugerindo um estado emocional moderado "
            f"ou ambíguo."
        )
    
    # Fallback
    return (
        f"📋 **Resumo**: Texto detectou **{text_em}** ({text_conf:.0f}%) e "
        f"imagem detectou **{image_em}** ({image_conf:.0f}%)."
    )


def _evaluate_consistency(
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult]
) -> str:
    """Avalia consistência entre emoções."""
    if not text_result or not image_result:
        return "N/A"
    
    _, text_cat = get_emotion_info(text_result.emotion)
    _, image_cat = get_emotion_info(image_result.emotion)
    
    if text_result.emotion.lower() == image_result.emotion.lower():
        return "✅ Consistente"
    
    if text_cat == image_cat:
        return "✅ Similar"
    
    return "❌ Divergente"


def load_llm_model():
    """Placeholder - não usa mais LLM externo."""
    return None


def analyze_with_local_llm(
    llm_pipe,  # Ignorado
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult]
) -> CombinedAnalysis:
    """Analisa resultados usando lógica inteligente."""
    interpretation = generate_interpretation(text_result, image_result)
    
    return CombinedAnalysis(
        text_emotion=text_result.emotion if text_result else "N/A",
        image_emotion=image_result.emotion if image_result else "N/A",
        summary=f"Texto: {text_result.emotion if text_result else 'N/A'} | Imagem: {image_result.emotion if image_result else 'N/A'}",
        interpretation=interpretation,
        consistency=_evaluate_consistency(text_result, image_result)
    )