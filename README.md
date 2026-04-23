# Climate Compare | Dashboard Global de Dados Climáticos

Um dashboard interativo que coleta, processa e visualiza dados climáticos em tempo real de qualquer cidade do mundo, permitindo comparações lado a lado.

## 🚀 Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar o dashboard
streamlit run dashboard/app.py
```

## 📝 Estrutura do Projeto

- `coleta/` — Coleta de dados via APIs
- `processamento/` — Limpeza e transformação dos dados
- `dashboard/` — Interface Streamlit
- `utils/` — Funções auxiliares
- `dados/` — Cache local de dados

## 🔌 APIs Utilizadas

- **Open-Meteo Forecast** — Previsão climática
- **Open-Meteo Geocoding** — Busca de cidades por nome

## 🛠️ Tecnologias

- Python 3.10+
- Streamlit
- Pandas
- Plotly
- Requests
