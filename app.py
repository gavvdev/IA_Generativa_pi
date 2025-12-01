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
from services.llm_combiner import analyze_with_local_llm
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
            <div class="footer-container">
                <div class="footer-info">
                    <div class="footer-section">
                        <h5>Colaboradores</h5>
                        <p>Carla Romero</p>
                        <p>Gabriela Pires</p>
                        <p>Lucas Emmanoel</p>
                        <p>Vitor Marins</p>
                    </div>
                    <div class="footer-section">
                        <h5>Modelos de ML</h5>
                        <a href="https://huggingface.co/unicamp-dl/translation-pt-en-t5" target="_blank">Tradução PT-EN</a>
                        <a href="https://huggingface.co/SamLowe/roberta-base-go_emotions" target="_blank">Emoção em Texto</a>
                        <a href="https://huggingface.co/dima806/facial_emotions_image_detection" target="_blank">Emoção Facial</a>
                    </div>
                    <div class="footer-section">
                        <h5>Suporte</h5>
                        <p>Entre em contato</p>
                        <p>Reporte erros</p>
                    </div>
                </div>
                <div class="footer-brand">
                    <strong>Classificador de Emoções</strong> · Python + Streamlit<br>
                        <a href="https://github.com/gavvdev/IA_Generativa_pi" target="_blank" style="display: inline-flex; align-items: center;">
                        <svg height="16" width="16" viewBox="0 0 16 16" style="margin-right: 6px; fill: currentColor;">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                        </svg>
                        Ver código no GitHub
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def main() -> None:
    """Função principal da aplicação."""
    st.set_page_config(page_title=UI.PAGE_TITLE, layout="wide")
    load_css()
    
    st.title(UI.APP_TITLE)
    st.write(UI.APP_DESCRIPTION)
    
    # Carrega modelos
    translation_pipe, text_emotion_pipe, facial_emotion_pipe = load_all_models()
    
    inputs = collect_inputs()
    
    if st.button("Analisar Emoções", type="primary"):
        if not inputs.has_text and not inputs.has_image:
            st.error(MESSAGES.NO_INPUT_ERROR)
            st.stop()
        
        text_result = None
        image_result = None
        llm_analysis = None
        
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
        
        # Análise combinada com LLM (apenas se tiver texto E imagem)
        if text_result and image_result:
            with st.spinner("Gerando análise integrada..."):
                llm_analysis = analyze_with_local_llm(
                    text_result,
                    image_result
                )
        
        render_results_tabs(text_result, image_result, inputs.use_grayscale, llm_analysis)
    
    render_footer()


if __name__ == "__main__":
    main()