# Classificador de Emoções com IA (Texto e Imagem)
<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

Aplicação web em Streamlit que utiliza modelos de IA da biblioteca `transformers` para:

- **Traduzir textos em Português para Inglês**
- **Classificar emoções em textos (modelo RoBERTa)**
- **Detectar emoções em rostos em imagens**

Tudo isso em uma interface simples, executada localmente com Streamlit.

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

## 🧠 Modelos de IA utilizados

A aplicação carrega e mantém em cache três pipelines principais da biblioteca `transformers`:

| Funcionalidade | Tarefa | Modelo |
|----------------|--------|--------|
| Tradução PT → EN | `translation` | `unicamp-dl/translation-pt-en-t5` |
| Classificação de emoções em texto | `text-classification` | `SamLowe/roberta-base-go_emotions` |
| Detecção de emoções faciais | `image-classification` | `dima806/facial_emotions_image_detection` |

Os modelos são inicializados apenas uma vez graças ao decorador `@st.cache_resource`, melhorando o desempenho.



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
IA_Generativa_pi/
├── components/              # Componentes da interface Streamlit
│   ├── __init__.py
│   ├── inputs.py            # Componentes de entrada (texto, imagem, opções)
│   └── results.py           # Componentes de exibição de resultados
├── config/                  # Configurações centralizadas
│   ├── __init__.py
│   └── settings.py          # Configurações de modelos, UI e mensagens
├── services/                # Serviços de processamento
│   ├── __init__.py
│   ├── image_processor.py   # Processamento e análise de imagens
│   ├── llm_combiner.py      # Combinação de análises com LLM
│   ├── model_loader.py      # Carregamento e cache dos modelos de IA
│   └── text_processor.py    # Tradução e análise de texto
├── styles/                  # Estilos personalizados
│   └── custom.css           # CSS customizado para a interface
├── .gitignore
├── README.md
├── requirements.txt         # Dependências do projeto
└── Streamlit.py             # Ponto de entrada da aplicação
```

## 🧾 Descrição dos Módulos

### [Streamlit.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/Streamlit.py:0:0-0:0)
Ponto de entrada da aplicação. Configura a página e orquestra o fluxo principal.

### [components/](cci:7://file:///c:/Users/User/IA_Generativa_pi/components:0:0-0:0)
- **[inputs.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/components/inputs.py:0:0-0:0)** - Renderiza campos de entrada: área de texto, upload de imagem e opções
- **[results.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/components/results.py:0:0-0:0)** - Exibe resultados em abas com métricas e interpretações

### [config/](cci:7://file:///c:/Users/User/IA_Generativa_pi/config:0:0-0:0)
- **[settings.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/config/settings.py:0:0-0:0)** - Configurações centralizadas: modelos, UI e mensagens do sistema

### [services/](cci:7://file:///c:/Users/User/IA_Generativa_pi/services:0:0-0:0)
- **[model_loader.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/model_loader.py:0:0-0:0)** - Carrega e cacheia os pipelines de IA
- **[text_processor.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/text_processor.py:0:0-0:0)** - Traduz texto PT→EN e classifica emoções
- **[image_processor.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/image_processor.py:0:0-0:0)** - Processa imagens e detecta emoções faciais
- **[llm_combiner.py](cci:7://file:///c:/Users/User/IA_Generativa_pi/services/llm_combiner.py:0:0-0:0)** - Combina análises de texto e imagem com interpretação

## 👥 Colaboradores

[![Contribuidores](https://img.shields.io/github/contributors/gavvdev/IA_Generativa_pi?color=blue)](https://github.com/gavvdev/IA_Generativa_pi/graphs/contributors)

<a href="https://github.com/gavvdev/IA_Generativa_pi/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=gavvdev/IA_Generativa_pi" />
</a>
