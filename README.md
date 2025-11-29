<div align="center">

# 🎭 Emotion Classifier AI

### Classificador de Emoções com Inteligência Artificial

**Análise de sentimentos em texto e detecção de emoções faciais em imagens**

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/🤗_Transformers-Powered-FFD21E?style=for-the-badge" alt="Transformers">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<p>
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-demonstração">Demo</a> •
  <a href="#-instalação">Instalação</a> •
  <a href="#-modelos-de-ia">Modelos</a> •
  <a href="#-estrutura">Estrutura</a>
</p>

---

</div>

## ✨ Funcionalidades

<table>
<tr>
<td width="50%">

### 📝 Análise de Texto
- Tradução automática PT → EN
- Classificação de emoções com RoBERTa
- Detecção de múltiplas emoções
- Índice de confiança em %

</td>
<td width="50%">

### 🖼️ Análise de Imagem
- Detecção de rostos automática
- Classificação de emoções faciais
- Suporte a PNG, JPG, JPEG, WebP
- Processamento em tempo real

</td>
</tr>
</table>


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
Os resultados são exibidos em seções separadas para texto e imagem e uma seção combinada das duas respostas, incluindo a emoção detectada e a confiança (%)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
   📝 Digite um texto ──► 🔄 Tradução ──► 🎭 Emoção ──►  (PT-BR) (PT→EN) detectada  
   🖼️ Upload de imagem ──► 👤 Detecção ──► 😊 Emoção ──► (rosto) facial identificada
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 🧠 Modelos de IA utilizados

A aplicação carrega e mantém em cache três pipelines principais da biblioteca `transformers`:

| Funcionalidade | Tarefa | Modelo |
|----------------|--------|--------|
| Tradução PT → EN | `translation` | `unic'amp-dl/translation-pt-en-t5` |
| Classificação de emoções em texto | `text-classification` | `SamLowe/roberta-base-go_emotions` |
| Detecção de emoções faciais | `image-classification` | `dima806/facial_emotions_image_detection` |

> 💡 **Performance:** Os modelos são carregados uma única vez usando `@st.cache_resource`, garantindo respostas rápidas após o carregamento inicial.

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

## 📁 Estrutura do Projeto
```
📦 IA_Generativa_pi/
│
├── 🎨 components/               # Componentes UI
│   ├── __init__.py
│   ├── inputs.py               # Entrada de dados
│   └── results.py              # Exibição de resultados
│
├── ⚙️ config/                   # Configurações
│   ├── __init__.py
│   └── settings.py             # Modelos, UI, mensagens
│
├── 🤖 services/                 # Serviços de IA
│   ├── __init__.py
│   ├── model_loader.py         # Cache dos modelos
│   ├── text_processor.py       # Tradução + análise texto
│   ├── image_processor.py      # Análise de imagens
│   └── llm_combiner.py         # Combinação de análises
│
├── 🎭 styles/
│   └── custom.css              # Estilos customizados
│
├── 📄 Streamlit.py              # Ponto de entrada
├── 📋 requirements.txt          # Dependências
└── 📖 README.md
```

## 🧾 Descrição dos Módulos

#### [Streamlit.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/Streamlit.py:0:0-0:0)  →  Ponto de entrada da aplicação. Configura a página e orquestra o fluxo principal.

#### [components/](cci:7://file:///c:/Users/User/IA_Generativa_pi/components:0:0-0:0)
- **[inputs.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/components/inputs.py:0:0-0:0)** → Renderiza campos de entrada: área de texto, upload de imagem e opções
- **[results.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/components/results.py:0:0-0:0)** → Exibe resultados em abas com métricas e interpretações

#### [config/](cci:7://file:///c:/Users/User/IA_Generativa_pi/config:0:0-0:0)
- **[settings.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/config/settings.py:0:0-0:0)** → Configurações centralizadas: modelos, UI e mensagens do sistema

#### [services/](cci:7://file:///c:/Users/User/IA_Generativa_pi/services:0:0-0:0)
- **[model_loader.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/model_loader.py:0:0-0:0)** - Carrega e cacheia os pipelines de IA
- **[text_processor.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/text_processor.py:0:0-0:0)** - Traduz texto PT→EN e classifica emoções
- **[image_processor.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/image_processor.py:0:0-0:0)** - Processa imagens e detecta emoções faciais
- **[llm_combiner.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/llm_combiner.py:0:0-0:0)** - Combina análises de texto e imagem com interpretação

## 👥 Colaboradores

[![Contribuidores](https://img.shields.io/github/contributors/gavvdev/IA_Generativa_pi?color=blue)](https://github.com/gavvdev/IA_Generativa_pi/graphs/contributors)

<a href="https://github.com/gavvdev/IA_Generativa_pi/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=gavvdev/IA_Generativa_pi" />
</a>

---

<p align="center">
⭐ Gostou do projeto? Deixe uma estrela!
              <br>
     Made with ❤️ and 🤖 AI
</p>
