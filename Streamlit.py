import streamlit as st
from transformers import pipeline

# ---- ESTRUTURA BASE ------

st.set_page_config(
    page_title="Classificador de Emoções"
)

st.title("Classificador de Emoções (IA)")
st.write("Insira o Texto e/ou carregue uma Imagem para análise de emoções.")

# --- ENTRADAS ---

st.subheader("Entrada de Texto")
texto_entrada = st.text_area(
    "Insira o Texto para Análise (Opcional):", 
    height=150, 
    placeholder="Digite sua frase aqui..."
)

st.subheader("Entrada de Imagem")
imagem_upload = st.file_uploader(
    "Carregue uma Imagem (PNG, JPG ou JPEG) (Opcional):", 
    type=['png', 'jpg', 'jpeg']
)

st.markdown("---") 

# --- LÓGICA DE PROCESSAMENTO ---

# Verifica se o texto foi preenchido
analisar_texto = bool(texto_entrada)
# Verifica se a imagem foi carregada
analisar_imagem = (imagem_upload is not None)

if st.button("Analisar Emoções", type="primary"):
    
    # 1. Verificação Mínima: Garante que pelo menos um campo for preenchido
    if not analisar_texto and not analisar_imagem:
        st.warning("Por favor, insira texto ou carregue uma imagem para iniciar a análise.")
        
    else:
        # 2.Roda se o texto existir
        if analisar_texto:
            st.subheader("Resultado da Análise de Texto")
            # ESPAÇO PARA LÓGICA DE CLASSIFICAÇÃO DE TEXTO
            st.success(f"Texto recebido para análise: '{texto_entrada}'")
        
        # 3. Separador, caso ambas as análises existam
        if analisar_texto and analisar_imagem:
            st.markdown("---")

        # 4.Roda se a imagem existir
        if analisar_imagem:
            # Se só a imagem for enviada, mas o resultado de texto não rodou,
            if not analisar_texto:
                 st.subheader("Resultado da Análise de Imagem")
            else:
                 st.subheader("Resultado da Análise de Imagem")
                 
            facial_pipe = pipeline("image-classification", model="dima806/facial_emotions_image_detection")

            facial_pipe(imagem_upload)
            st.success("Imagem carregada com sucesso para análise!")