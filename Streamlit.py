import streamlit as st
from transformers import pipeline
from PIL import Image
from io import BytesIO
import base64
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #262730;
        padding: 12px;
        border-radius: 12px;
        margin-top: 50px
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 12px 28px;
        background-color: #3d3d4d;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        color: white !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #4d4d5d;
    }
    .stTabs [aria-selected="true"]:hover {
        background-color: #ff6b6b !important;
    }
</style>
""", unsafe_allow_html=True)

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

def preprocessar_imagem_grayscale(image):
    """
    Converte a imagem para escala de cinza e de volta para RGB.
    Isso ajuda o modelo a focar nas características faciais,
    removendo informação de cor que pode ser ruído.
    """
    # Converte para escala de cinza (modo 'L' = luminância)
    grayscale = image.convert('L')
    # Converte de volta para RGB (3 canais) pois o modelo espera esse formato
    grayscale_rgb = grayscale.convert('RGB')
    return grayscale_rgb

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

usar_grayscale = st.checkbox("Usar pré-processamento em escala de cinza", value=False)

st.markdown("---") 

# --- LÓGICA DE PROCESSAMENTO ---

analisar_texto = bool(texto_entrada)
analisar_imagem = (imagem_upload is not None)

if st.button("Analisar Emoções", type="primary"):
    
    if not analisar_texto and not analisar_imagem:
        st.error("Por favor, insira texto ou carregue uma imagem para iniciar a análise.")
        st.stop()
    
    # Variáveis para armazenar resultados
    resultado_texto = None
    resultado_imagem = None
    
    # --- Processamento do Texto ---
    if analisar_texto:
        with st.spinner("Traduzindo e classificando texto..."):
            texto_traduzido = traduzir_texto(translation_pipe, texto_entrada)
            resultado_emocao = roberta_pipe(texto_traduzido)[0][0]
            emocao_principal = resultado_emocao['label']
            pontuacao = resultado_emocao['score'] * 100
            resultado_texto = {
                'original': texto_entrada,
                'traduzido': texto_traduzido,
                'emocao': emocao_principal,
                'pontuacao': pontuacao
            }
    
    # --- Processamento da Imagem ---
    if analisar_imagem:
        with st.spinner("Analisando emoções na imagem..."):
            image_bytes = imagem_upload.getvalue()
            image = Image.open(BytesIO(image_bytes))
            
            if usar_grayscale:
                image_processada = preprocessar_imagem_grayscale(image)
            else:
                image_processada = image
            
            resultado_facial = facial_pipe(image_processada)[0]
            emocao_facial = resultado_facial['label']
            pontuacao_facial = resultado_facial['score'] * 100
            resultado_imagem = {
                'image': image,
                'image_processada': image_processada,
                'emocao': emocao_facial,
                'pontuacao': pontuacao_facial,
                'nome': imagem_upload.name
            }
    
    # --- Exibição em Abas ---
    tab_texto, tab_imagem, tab_combinado = st.tabs(["Texto", "Imagem", "Combinado"])
    
    with tab_texto:
        if resultado_texto:
            st.subheader("Resultado da Análise de Texto")
            st.info(f"Texto original (PT): **{resultado_texto['original']}**")
            st.info(f"Texto traduzido (EN): *{resultado_texto['traduzido']}*")
            st.success(f"Emoção Detectada: **{resultado_texto['emocao'].upper()}** (Confiança: {resultado_texto['pontuacao']:.2f}%)")
        else:
            st.warning("Nenhum texto foi inserido para análise.")
    
    with tab_imagem:
        if resultado_imagem:
            st.subheader("Resultado da Análise de Imagem")
            st.success(f"Emoção Facial Detectada: **{resultado_imagem['emocao'].upper()}** (Confiança: {resultado_imagem['pontuacao']:.2f}%)")
            
            if usar_grayscale:
                st.image(resultado_imagem['image_processada'], caption=f"Imagem Processada (Grayscale): {resultado_imagem['nome']}", use_container_width=True)
            
            st.image(resultado_imagem['image'], caption=f"Imagem Original: {resultado_imagem['nome']}", use_container_width=True)
        else:
            st.warning("Nenhuma imagem foi carregada para análise.")
    
    with tab_combinado:
        if resultado_texto and resultado_imagem:
            st.subheader("Resultado Combinado")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Texto")
                st.info(f"**{resultado_texto['emocao'].upper()}** ({resultado_texto['pontuacao']:.2f}%)")
            
            with col2:
                st.markdown("### Imagem")
                st.info(f"**{resultado_imagem['emocao'].upper()}** ({resultado_imagem['pontuacao']:.2f}%)")
            
            st.markdown("---")
            st.image(resultado_imagem['image'], caption=resultado_imagem['nome'], use_container_width=True)
        else:
            st.warning("Insira texto E imagem para ver o resultado combinado.")

# --- RODAPÉ ---
st.markdown(
    """
    <style>
        .footer-full {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #111827;
            color: #9ca3af;
            text-align: center;
            padding: 0.6rem 0;
            font-size: 0.8rem;
            z-index: 9999;
        }
        .footer-full a {
            color: #60a5fa;
            text-decoration: none;
        }
        .footer-full a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer-full">
        Projeto <strong>Classificador de Emoções com IA</strong> ·
        Desenvolvido em Python + Streamlit · Modelos Hugging Face ·
        <a href="https://github.com/gavvdev/IA_Generativa_pi" target="_blank">Ver código no GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)