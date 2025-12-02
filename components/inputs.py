"""Componentes de entrada da interface."""
from typing import Optional, Tuple
from dataclasses import dataclass

import streamlit as st

from config.settings import UI


@dataclass
class UserInputs:
    """Container para todas as entradas do usuário."""
    text: str
    image_file: Optional[object]
    use_grayscale: bool
    use_gemini: bool
    
    @property
    def has_text(self) -> bool:
        return bool(self.text)
    
    @property
    def has_image(self) -> bool:
        return self.image_file is not None


def render_text_input() -> str:
    """Renderiza área de entrada de texto."""
    st.subheader("Entrada de Texto")
    return st.text_area(
        "Insira o Texto para Análise:",
        height=150,
        placeholder="Digite seu texto aqui em Português..."
    )


def render_image_input() -> Optional[object]:
    """Renderiza upload de imagem."""
    st.subheader("Entrada de Imagem")
    return st.file_uploader(
        "Carregue uma Imagem (PNG, JPG, JPEG, WEBP):",
        type=list(UI.SUPPORTED_IMAGE_TYPES)
    )


def render_options() -> Tuple[bool, bool]:
    """Renderiza opções de processamento."""
    grayscale = st.checkbox("Usar pré-processamento em escala de cinza", value=False)
    use_gemini = st.checkbox("Usar análise integrada com Gemini (IA)", value=True)
    return grayscale, use_gemini


def collect_inputs() -> UserInputs:
    """Coleta todas as entradas do usuário."""
    text = render_text_input()
    image = render_image_input()
    grayscale, use_gemini = render_options()
    st.markdown("---")
    
    return UserInputs(text=text, image_file=image, use_grayscale=grayscale, use_gemini=use_gemini)