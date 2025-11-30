"""Componentes de exibição de resultados."""
from typing import Optional

import streamlit as st

from services.text_processor import TextResult
from services.image_processor import ImageResult
from services.llm_combiner import CombinedAnalysis
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
        
        st.image(
            result.original_image,
            caption=f"Imagem Original: {result.filename}",
            use_container_width=True
        )

        if show_grayscale:
            st.image(
                result.processed_image,
                caption=f"Imagem Processada (Grayscale): {result.filename}",
                use_container_width=True
            )
        
    else:
        st.warning(MESSAGES.NO_IMAGE_WARNING)


def render_llm_analysis(analysis: CombinedAnalysis) -> None:
    """Renderiza análise do LLM."""
    st.subheader("Análise Integrada por IA")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Emoção Texto", analysis.text_emotion.upper())
    with col2:
        st.metric("Emoção Imagem", analysis.image_emotion.upper())
    with col3:
        st.metric("Consistência", analysis.consistency)
    
    st.markdown("---")
    st.markdown("### 💡 Interpretação")
    st.info(analysis.interpretation)
    st.info(f"🤖 **Análise do LLM**: {analysis.llm_summary}")


def render_results_tabs(
    text_result: Optional[TextResult],
    image_result: Optional[ImageResult],
    show_grayscale: bool,
    llm_analysis: Optional[CombinedAnalysis] = None
) -> None:
    """Renderiza abas com todos os resultados."""
    tabs = ["Texto", "Imagem"]
    if llm_analysis:
        tabs.append("Análise IA")
    
    tab_list = st.tabs(tabs)
    
    with tab_list[0]:
        render_text_result(text_result)
    
    with tab_list[1]:
        render_image_result(image_result, show_grayscale)
    
    if llm_analysis and len(tab_list) > 2:
        with tab_list[2]:
            render_llm_analysis(llm_analysis)