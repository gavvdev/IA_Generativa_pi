"""
Classificador de Emoções - Aplicação Principal.

Análise de emoções em texto (português) e imagens faciais
utilizando modelos de IA da Hugging Face.
"""
from pathlib import Path

import streamlit as st

from config.settings import UI, MESSAGES
from services.model_loader import load_all_models
from services.text_processor import analyze_text_emotion
from services.image_processor import analyze_facial_emotion
from components.inputs import collect_inputs
from components.results import render_results_tabs


def load_css() -> None:
    """Carrega estilos CSS customizados."""
    css_path = Path(__file__).parent / "styles" / "custom.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def render_footer() -> None:
    """Renderiza rodapé da aplicação."""
    st.markdown(
        """
        <div class="footer-full">
            Projeto <strong>Classificador de Emoções com IA</strong> ·
            Desenvolvido em Python + Streamlit · Modelos Hugging Face ·
            <a href="https://github.com/gavvdev/IA_Generativa_pi" target="_blank">
                Ver código no GitHub
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Função principal da aplicação."""
    # Configuração da página (DEVE ser o primeiro comando Streamlit)
    st.set_page_config(page_title=UI.PAGE_TITLE)
    
    # Carrega estilos
    load_css()
    
    # Header
    st.title(UI.APP_TITLE)
    st.write(UI.APP_DESCRIPTION)
    
    # Carrega modelos
    translation_pipe, text_emotion_pipe, facial_emotion_pipe = load_all_models()
    
    # Coleta entradas
    inputs = collect_inputs()
    
    # Botão de análise
    if st.button("Analisar Emoções", type="primary"):
        if not inputs.has_text and not inputs.has_image:
            st.error(MESSAGES.NO_INPUT_ERROR)
            st.stop()
        
        text_result = None
        image_result = None
        
        # Processa texto
        if inputs.has_text:
            with st.spinner(MESSAGES.TRANSLATING):
                text_result = analyze_text_emotion(
                    translation_pipe,
                    text_emotion_pipe,
                    inputs.text
                )
        
        # Processa imagem
        if inputs.has_image:
            with st.spinner(MESSAGES.ANALYZING_IMAGE):
                image_result = analyze_facial_emotion(
                    facial_emotion_pipe,
                    inputs.image_file.getvalue(),
                    inputs.image_file.name,
                    inputs.use_grayscale
                )
        
        # Exibe resultados
        render_results_tabs(text_result, image_result, inputs.use_grayscale)
    
    # Rodapé
    render_footer()


if __name__ == "__main__":
    main()