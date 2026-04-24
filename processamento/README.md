"""
Processamento module - Data transformation

IMPORTANTE: Estes arquivos foram refatorados para integração com Django.
As seguintes melhorias estão planejadas:

1. Integração com models.py para persistência
2. Cache de transformações
3. Validação de dados com schemas
4. Logging de transformações
5. Tratamento de valores nulos/inválidos
6. Performance optimization (vectorização com numpy)
7. Testes unitários
8. Type hints completos
9. Docstrings em Google Format

Para usar o processador, importe diretamente:
    from processamento.transformar import ProcessadorClima, processar_api

Ou acesse via API:
    GET /api/v1/weather/forecasts/
"""
