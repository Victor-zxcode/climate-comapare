# Climate Compare - Django Project

Um dashboard profissional para comparar dados climáticos de múltiplas cidades em tempo real.

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.10+
- pip
- virtualenv

### Instalação

```bash
# 1. Clone o repositório
git clone <seu-repositorio>
cd climate-compare

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env conforme necessário

# 6. Execute as migrações
python manage.py migrate

# 7. Crie um superusuário
python manage.py createsuperuser

# 8. Colete arquivos estáticos
python manage.py collectstatic --noinput

# 9. Execute o servidor de desenvolvimento
python manage.py runserver
```

Acesse o dashboard em `http://localhost:8000`

## 📁 Estrutura do Projeto

```
climate-compare/
├── config/                      # Configurações Django
│   ├── settings/
│   │   ├── base.py             # Configurações compartilhadas
│   │   ├── development.py      # Desenvolvimento
│   │   └── production.py       # Produção
│   ├── urls.py                 # URLs principais
│   ├── wsgi.py                 # WSGI para produção
│   └── asgi.py                 # ASGI para async
│
├── apps/                        # Aplicações Django
│   ├── weather/                # App de clima
│   │   ├── models.py           # Modelos de dados
│   │   ├── views.py            # ViewSets da API
│   │   ├── serializers.py      # Serializers DRF
│   │   ├── urls.py             # URLs da app
│   │   └── tests.py            # Testes
│   │
│   ├── cities/                 # App de cidades
│   │   └── ...
│   │
│   └── api/                    # Configuração da API
│       ├── v1/                 # API v1
│       └── urls.py             # URLs da API
│
├── core/                        # Código compartilhado
│   ├── utils.py                # Funções auxiliares
│   ├── exceptions.py           # Exceções customizadas
│   ├── constants.py            # Constantes
│   └── mixins.py               # Mixins de modelo
│
├── coleta/                      # Clientes de APIs externas
│   ├── api_client.py           # Open-Meteo API
│   └── geocoding.py            # Geocoding API
│
├── processamento/               # Processamento de dados
│   └── transformar.py          # Transformações de dados
│
├── templates/                   # Templates HTML
│   ├── base.html               # Template base
│   ├── index.html              # Página inicial
│   └── includes/               # Includes reutilizáveis
│
├── static/                      # Arquivos estáticos
│   ├── css/
│   │   └── style.css           # Estilos customizados
│   └── js/
│       └── main.js             # JavaScript compartilhado
│
├── logs/                        # Logs da aplicação
├── manage.py                    # Gerenciador Django
├── requirements.txt             # Dependências
├── .env.example                 # Exemplo de variáveis
└── README.md                    # Este arquivo
```

## 🔌 APIs Utilizadas

### Open-Meteo Forecast API
Previsões climáticas e dados históricos
- **Base URL**: `https://api.open-meteo.com/v1/forecast`
- **Documentação**: https://open-meteo.com/

### Open-Meteo Geocoding API
Busca e geocodificação de cidades
- **Base URL**: `https://geocoding-api.open-meteo.com/v1/search`

## 🛠️ Tecnologias

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Frontend**: Bootstrap 5 + Plotly.js
- **APIs**: Open-Meteo
- **Task Queue**: Celery (opcional)
- **Cache**: Redis (produção) / Local (desenvolvimento)
- **Monitoring**: Sentry (opcional)

## 📊 Endpoints da API

### Weather
- `GET /api/v1/weather/forecasts/` - Listar previsões
- `GET /api/v1/weather/forecasts/{id}/` - Detalhe de previsão
- `GET /api/v1/weather/comparisons/` - Listar comparações
- `POST /api/v1/weather/comparisons/` - Criar comparação

### Cities
- `GET /api/v1/cities/` - Listar cidades
- `GET /api/v1/cities/{id}/` - Detalhe de cidade
- `GET /api/v1/cities/?search=brasilia` - Buscar cidades

## 🔐 Segurança

- CSRF protection habilitado
- SQL Injection protection através do ORM
- XSS protection habilitado
- CORS configurável
- Rate limiting (recomendado para produção)

## 🚀 Deploy

### Produção com Gunicorn

```bash
# Instale Gunicorn
pip install gunicorn

# Configure .env com settings de produção
DJANGO_SETTINGS_MODULE=config.settings.production

# Execute
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Docker

```bash
docker build -t climate-compare .
docker run -p 8000:8000 climate-compare
```

## 📝 Boas Práticas Implementadas

- ✅ Arquitetura em camadas (Models, Serializers, Views)
- ✅ Separação clara entre settings (dev, prod, test)
- ✅ Logging configurado por ambiente
- ✅ Type hints em funções críticas
- ✅ Tratamento de exceções customizadas
- ✅ Testes unitários
- ✅ Documentação de código
- ✅ Code style (flake8, black, isort)
- ✅ Variáveis de ambiente isoladas
- ✅ Migrations automáticas

## 🧪 Testes

```bash
# Rodar todos os testes
python manage.py test

# Rodar com coverage
pytest --cov=apps --cov-report=html

# Rodar um test específico
python manage.py test apps.weather.tests.WeatherForecastTestCase
```

## 📋 Commands Disponíveis

```bash
# Migrações
python manage.py makemigrations
python manage.py migrate

# Admin
python manage.py createsuperuser

# Shell
python manage.py shell

# Estáticos
python manage.py collectstatic

# Linting
flake8 apps/ core/
black apps/ core/ config/
isort apps/ core/ config/
```

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 🆘 Suporte

Para suporte, abra uma issue no repositório.

## 📧 Contato

Email: seu-email@example.com  
GitHub: [@seu-usuario](https://github.com/seu-usuario)
