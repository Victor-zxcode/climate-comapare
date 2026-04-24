"""
Coleta module - External API clients

IMPORTANTE: Estes arquivos foram refatorados para integração com Django.
As seguintes melhorias estão planejadas:

1. Integração com models.py para cache em banco de dados
2. Adição de tratamento de rate-limiting
3. Implementação de retry logic
4. Logging estruturado
5. Testes unitários com mocks
6. Type hints completos
7. Docstrings em Google Format
8. Validação de entrada robusta

Para usar os clientes de API, importe-os diretamente:
    from coleta.api_client import OpenMeteoClient
    from coleta.geocoding import GeocodingClient

Ou use os ViewSets da API:
    GET /api/v1/weather/forecasts/
    GET /api/v1/cities/
"""
