"""Componentes de exibição de resultados."""
from typing import Optional

import streamlit as st

from services.text_processor import TextResult
from services.image_processor import ImageResult
from config.settings import MESSAGES


def render_text_result(result: Optional[TextResult]) -> None:
    """Renderiza resultado da análise de texto."""
    if result:
        st.subheader("Resultado da Análise de Texto")
        st.info(f"Texto original (PT): **{result.original}**")
        st.info(f"Texto traduzido (EN): *{result.translated}*")
        st.success(
            f"Emoção Detectada: **{result.emotion.upper()}** "
            f"(Confiança: {result.confidence:.2f}%)"
        )
    else:
        st.warning(MESSAGES.NO_TEXT_WARNING)


def render_image_result(result: Optional[ImageResult], show_grayscale: bool) -> None:
    """Renderiza resultado da análise de imagem."""
    if result:
        st.subheader("Resultado da Análise de Imagem")
        st.success(
            f"Emoção Facial Detectada: **{result.emotion.upper()}** "
            f"(Confiança: {result.confidence:.2f}%)"
        )
        
        if show_grayscale:
            st.image(
                result.processed_image,
                caption=f"Imagem Processada (Grayscale): {result.filename}",
                use_container_width=True
            )
        
        st.image(
            result.original_image,
            caption=f"Imagem Original: {result.filename}",
            use_container_width=True
        )
    else:
        st.warning(MESSAGES.NO_IMAGE_WARNING)


def render_combined_result(
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult]
) -> None:
    """Renderiza resultado combinado."""
    if text_result and image_result:
        st.subheader("Resultado Combinado")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Texto")
            st.info(f"**{text_result.emotion.upper()}** ({text_result.confidence:.2f}%)")
        
        with col2:
            st.markdown("### Imagem")
            st.info(f"**{image_result.emotion.upper()}** ({image_result.confidence:.2f}%)")
        
        st.markdown("---")
        st.image(
            image_result.original_image,
            caption=image_result.filename,
            use_container_width=True
        )
    else:
        st.warning(MESSAGES.COMBINED_WARNING)


def render_results_tabs(
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult],
    show_grayscale: bool
) -> None:
    """Renderiza abas com todos os resultados."""
    tab_texto, tab_imagem, tab_combinado = st.tabs(["Texto", "Imagem", "Combinado"])
    
    with tab_texto:
        render_text_result(text_result)
    
    with tab_imagem:
        render_image_result(image_result, show_grayscale)
    
    with tab_combinado:
        render_combined_result(text_result, image_result)