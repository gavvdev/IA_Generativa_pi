"""Serviço de carregamento e cache de modelos de IA."""
from typing import Tuple
import streamlit as st
from transformers import Pipeline, pipeline

from config.settings import MODELS, MESSAGES


@st.cache_resource
def load_all_models() -> Tuple[Pipeline, Pipeline, Pipeline]:
    """
    Carrega e cacheia todos os modelos de IA necessários.
    
    Returns:
        Tuple contendo os pipelines de tradução, classificação de texto e facial.
    """
    with st.spinner(MESSAGES.LOADING_MODELS):
        translation_pipe = pipeline(
            "translation",
            model=MODELS.TRANSLATION_MODEL
        )
        
        text_emotion_pipe = pipeline(
            "text-classification",
            model=MODELS.TEXT_EMOTION_MODEL,
            top_k=1
        )
        
        facial_emotion_pipe = pipeline(
            "image-classification",
            model=MODELS.FACIAL_EMOTION_MODEL,
            top_k=1
        )
    
    return translation_pipe, text_emotion_pipe, facial_emotion_pipe