"""Serviço de combinação de resultados usando análise inteligente."""
from dataclasses import dataclass
from typing import Optional
import os
import streamlit as st

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_TOKEN")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")

client = genai.Client(api_key=GEMINI_API_KEY)

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
    llm_summary: str = "N/A"


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
    "approval": ("Aprovação", "positiva"),
    "caring": ("Carinho", "positiva"),
    "desire": ("Desejo", "positiva"),
    "excitement": ("Entusiasmo", "positiva"),
    "gratitude": ("Gratidão", "positiva"),
    "nervousness": ("Nervosismo", "positiva"),
    "pride": ("Orgulho", "positiva"),
    "realization": ("Realização", "positiva"),
    "relief": ("Alívio", "positiva"),
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
    "annoyance": ("Irritação", "negativa"),
    "disapproval": ("Desaprovação", "negativa"),
    "disgust": ("Desgosto", "negativa"),
    "embarrassment": ("Vergonha", "negativa"),
    "fear": ("Medo", "negativa"),
    "remorse": ("Remorso", "negativa"),
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


def load_llm_model(
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult]
):
    """Carrega e executa o modelo LLM para análise combinada."""
    if not text_result or not image_result:
        return None
    
    text_em, _ = get_emotion_info(text_result.emotion)
    image_em, _ = get_emotion_info(image_result.emotion)
    text_conf = text_result.confidence
    image_conf = image_result.confidence
    text_content = text_result.original

    llm_response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            system_instruction="Você deverá analisar as emoções faciais de um indivíduo e a emoção da fala do mesmo, e então você deverá explicar a possivel explicação para a combinação dessas emoções. Seja claro e conciso em sua resposta, explique tudo em um só parágrafo.",),
        contents=f'A emoção facial é "{image_em}" com confiança de "{image_conf}%". A emoção do texto é "{text_em}" com confiança de "{text_conf}%". O conteuro do do texto é: "{text_content}"'
    )
    return llm_response


def analyze_with_local_llm(
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult]
) -> CombinedAnalysis:
    """Analisa resultados usando lógica inteligente."""
    interpretation = generate_interpretation(text_result, image_result)

    # Chama o LLM
    llm_response = load_llm_model(text_result, image_result)

    llm_summary = "N/A"
    if llm_response and hasattr(llm_response, 'content'):
        llm_summary = llm_response.text
    elif llm_response and hasattr(llm_response, 'candidates'):
        llm_summary = llm_response.candidates[0].content.parts[0].text if llm_response.candidates else "N/A"
    
    return CombinedAnalysis(
        text_emotion=text_result.emotion if text_result else "N/A",
        image_emotion=image_result.emotion if image_result else "N/A",
        summary=f"Texto: {text_result.emotion if text_result else 'N/A'} | Imagem: {image_result.emotion if image_result else 'N/A'}",
        interpretation=interpretation,
        consistency=_evaluate_consistency(text_result, image_result),
        llm_summary=llm_summary
    )