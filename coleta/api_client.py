"""
api_client.py - Cliente para a Open-Meteo Forecast API

Módulo responsável por fazer requisições à API Open-Meteo
e retornar dados climáticos (temperatura, chuva, vento, umidade)
para uma coordenada geográfica específica.
"""

import requests
import json
from typing import Dict, Optional


class OpenMeteoClient:
    """Cliente para comunicação com a Open-Meteo Forecast API"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.session = requests.Session()
        self.timeout = 10  # segundos
    
    def obter_previsao(
        self, 
        latitude: float, 
        longitude: float, 
        dias: int = 7,
        idioma: str = "pt"
    ) -> Optional[Dict]:
        """
        Obtém previsão climática para uma coordenada.
        
        Args:
            latitude: Latitude do local (-90 a 90)
            longitude: Longitude do local (-180 a 180)
            dias: Número de dias de previsão (máx 16)
            idioma: Idioma dos resultados
        
        Returns:
            Dicionário com dados climáticos ou None se falhar
        """
        
        # Validar entrada
        if dias > 16:
            dias = 16
        
        # Parâmetros da requisição
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,precipitation,windspeed_10m,relativehumidity_2m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
            "forecast_days": dias,
            "timezone": "auto"
        }
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            print(f"❌ Timeout ao conectar com Open-Meteo")
            return None
        
        except requests.exceptions.ConnectionError:
            print(f"❌ Erro de conexão com Open-Meteo")
            return None
        
        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro HTTP: {e.response.status_code}")
            return None
        
        except Exception as e:
            print(f"❌ Erro ao obter previsão: {str(e)}")
            return None
    
    def obter_temperatura_agora(self, latitude: float, longitude: float) -> Optional[float]:
        """
        Retorna a temperatura atual (primeira hora dos dados horários).
        
        Args:
            latitude: Latitude
            longitude: Longitude
        
        Returns:
            Temperatura em °C ou None
        """
        dados = self.obter_previsao(latitude, longitude, dias=1)
        
        if dados and "hourly" in dados and "temperature_2m" in dados["hourly"]:
            return dados["hourly"]["temperature_2m"][0]
        
        return None


# Função auxiliar (para uso simples, sem classe)
def get_forecast(latitude: float, longitude: float, days: int = 7) -> Optional[Dict]:
    """
    Função simples para obter previsão climática.
    
    Uso: dados = get_forecast(-15.78, -47.89)
    """
    client = OpenMeteoClient()
    return client.obter_previsao(latitude, longitude, dias=days)
