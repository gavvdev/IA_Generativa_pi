import streamlit as st
from transformers import pipeline
from PIL import Image
from io import BytesIO
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Classificador de Emoções"
)

st.title("Classificador de Emoções (IA)")
st.write("Insira o Texto e/ou carregue uma Imagem para análise de emoções.")

# --- INICIALIZAÇÃO E CACHE DE MODELOS ---

@st.cache_resource
def load_models():
    """
    otimização de desempenho).
    """
    
    with st.spinner('Carregando modelos de IA...'):
        # 1. Modelo de Tradução PT -> EN
        translation_pipe = pipeline(
            "translation", 
            model="unicamp-dl/translation-pt-en-t5"
        )
        
        # 2. Modelo de Classificação de Emoções de Texto (RoBERTa - funciona apenas em EN)
        roberta_pipe = pipeline(
            "text-classification", 
            model="SamLowe/roberta-base-go_emotions", 
            top_k=1 
        )
        
        # 3. Modelo de Reconhecimento Facial de Emoções (Image Classification)
        facial_pipe = pipeline(
            "image-classification", 
            model="dima806/facial_emotions_image_detection", 
            top_k=1
        )
        
    return translation_pipe, roberta_pipe, facial_pipe

# Carrega os modelos uma vez na inicialização
translation_pipe, roberta_pipe, facial_pipe = load_models()


def traduzir_texto(pipe, input_texto):
    """Traduz o texto de Português para Inglês usando o pipeline T5."""
    texto_com_comando = f"translate Portuguese to English: {input_texto}"
    
    output = pipe(
        texto_com_comando,
        src_lang='portuguese',
        tgt_lang='english',
        max_length=400
    )
    return output[0]['translation_text']


# --- ENTRADAS DA INTERFACE ---

st.subheader("Entrada de Texto")
texto_entrada = st.text_area(
    "Insira o Texto para Análise:", 
    height=150, 
    placeholder="Digite seu texto aqui em Português..."
)

st.subheader("Entrada de Imagem")
imagem_upload = st.file_uploader(
    "Carregue uma Imagem (PNG, JPG, JPEG, WEBP):", 
    type=['png', 'jpg', 'jpeg', 'webp']
)

st.markdown("---") 

# --- LÓGICA DE PROCESSAMENTO ---

analisar_texto = bool(texto_entrada)
analisar_imagem = (imagem_upload is not None)

if st.button("Analisar Emoções", type="primary"):
    
    if not analisar_texto and not analisar_imagem:
        st.error("Por favor, insira texto ou carregue uma imagem para iniciar a análise.")
        st.stop()
        
    # Lógica de Análise de Texto
    if analisar_texto:
        with st.spinner("Traduzindo e classificando texto..."):
            
            # 1. Tradução PT -> EN
            texto_traduzido = traduzir_texto(translation_pipe, texto_entrada)
            
            # 2. Análise de Emoção
            resultado_emocao = roberta_pipe(texto_traduzido)[0][0]
            
            # 3. Formatar saída
            emocao_principal = resultado_emocao['label']
            pontuacao = resultado_emocao['score'] * 100
            
            st.subheader("Resultado da Análise de Texto")
            st.info(f"Texto original (PT): **{texto_entrada}**")
            st.info(f"Texto traduzido (EN): *{texto_traduzido}*")
            st.success(f"Emoção Detectada: **{emocao_principal.upper()}** (Confiança: {pontuacao:.2f}%)")
    
    # Separador, caso ambas as análises existam
    if analisar_texto and analisar_imagem:
        st.markdown("---")

    # Lógica de Análise de Imagem (Roda se a imagem existir)
    if analisar_imagem:
        if not analisar_texto:
            st.subheader("Resultado da Análise de Imagem")
        else:
            st.subheader("Resultado da Análise de Imagem")
        
        # Cria um placeholder para o resultado da IA acima da imagem
        placeholder_ia_imagem = st.empty() 
        
        with st.spinner("Analisando emoções na imagem..."):
            
            # 1. Preparar Imagem (converter bytes de upload para objeto PIL Image)
            image_bytes = imagem_upload.getvalue()
            image = Image.open(BytesIO(image_bytes))
            
            # 2. Análise Facial
            resultado_facial = facial_pipe(image)[0]
            
            # 3. Formatar saída
            emocao_facial = resultado_facial['label']
            pontuacao_facial = resultado_facial['score'] * 100
        
        # Exibição da Imagem (Abaixo do placeholder)
        st.image(
            image, 
            caption=f'Imagem Carregada: {imagem_upload.name}', 
            use_container_width=True
        )
        
        # Preenchendo o espaço reservado com o resultado
        placeholder_ia_imagem.success(f"Emoção Facial Detectada: **{emocao_facial.upper()}** (Confiança: {pontuacao_facial:.2f}%)")