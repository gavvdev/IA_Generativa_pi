# Classificador de Emoções com IA (Texto e Imagem)
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

Aplicação web em Streamlit que utiliza modelos de IA da biblioteca `transformers` para:

- **Traduzir textos em Português para Inglês**
- **Classificar emoções em textos (modelo RoBERTa)**
- **Detectar emoções em rostos em imagens**

Tudo isso em uma interface simples, executada localmente com Streamlit.

---

## 🚀 Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone [https://github.com/gavvdev/IA_Generativa_pi.git](https://github.com/gavvdev/IA_Generativa_pi.git)
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Executar a aplicação usando o Streamlit
```bash
py -m streamlit run Streamlit.py
```


## 🧠 Modelos de IA utilizados
A aplicação carrega e mantém em cache três pipelines principais da biblioteca transformers:

- Tradução PT → EN
  - Tarefa: translation
  - Modelo: unicamp-dl/translation-pt-en-t5

- Classificação de emoções em texto (Inglês)
  - Tarefa: text-classification
  - Modelo: SamLowe/roberta-base-go_emotions

- Detecção de emoções faciais em imagens
  - Tarefa: image-classification
  - Modelo: dima806/facial_emotions_image_detection

Os modelos são inicializados apenas uma vez graças ao decorador 
``` st.cache_resource```, melhorando o desempenho.

## 🖥️ Como usar a interface

- O usuário precisa digitar um Texto (opcional)
  - Digite um texto em Português na área de texto.
  - O sistema traduz o texto para Inglês e em seguida classifica a emoção principal.

- Imagem (opcional)
  - Faça upload de uma imagem (.png, .jpg, .jpeg, .webp).
  - O sistema analisa o rosto na imagem e identifica a emoção predominante.
- Botão "Analisar Emoções"
  - Você pode:
    - Enviar apenas texto,
    - Enviar apenas imagem,
    - Ou ambos ao mesmo tempo.

Se nada for enviado, a aplicação mostra uma mensagem de erro pedindo entrada.
Os resultados são exibidos em seções separadas para texto e imagem, incluindo a emoção detectada e a confiança (%)

## 🧾 Estrutura principal do código

- **[Streamlit.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/Streamlit.py:0:0-0:0)**
  - **Configuração da página Streamlit**
  - **Função [load_models()](cci:1://file:///c:/Users/User/IA_Generativa_pi/Streamlit.py:16:0-43:54) para carregar:**
    - Pipeline de tradução
    - Pipeline de classificação de emoções em texto
    - Pipeline de emoções em imagens
  - **Função [traduzir_texto()](cci:1://file:///c:/Users/User/IA_Generativa_pi/Streamlit.py:49:0-59:40)** para preparar o prompt e chamar o modelo T5
  - **Lógica de interface** (`st.text_area`, `st.file_uploader`, `st.button`)
  - **Lógica de processamento para:**
    - Tradução + classificação de texto
    - Análise de imagem com o modelo facial

## 👥 Colaboradores

[![Contribuidores](https://img.shields.io/github/contributors/gavvdev/IA_Generativa_pi?color=blue)](https://github.com/gavvdev/IA_Generativa_pi/graphs/contributors)

<a href="https://github.com/gavvdev/IA_Generativa_pi/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=gavvdev/IA_Generativa_pi" />
</a>
