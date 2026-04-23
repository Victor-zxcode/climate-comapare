"""
geocoding.py - Conversão de nomes de cidades em coordenadas

Módulo que usa a Open-Meteo Geocoding API para converter
nomes de cidades ou países em suas coordenadas (latitude/longitude).
"""

import requests
from typing import Dict, List, Optional


class GeocodingClient:
    """Cliente para a Open-Meteo Geocoding API"""
    
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    
    def __init__(self):
        self.session = requests.Session()
        self.timeout = 10  # segundos
    
    def buscar_cidade(
        self,
        nome: str,
        limite: int = 5,
        idioma: str = "pt"
    ) -> Optional[List[Dict]]:
        """
        Busca uma cidade por nome e retorna resultados com coordenadas.
        
        Args:
            nome: Nome da cidade ou país
            limite: Número máximo de resultados (padrão: 5)
            idioma: Idioma dos resultados (pt, en, es, etc)
        
        Returns:
            Lista de dicionários com cidades encontradas ou None se falhar
            
        Exemplo:
            resultados = buscar_cidade("Brasília")
            # [{"name": "Brasília", "latitude": -15.78, "longitude": -47.89, ...}]
        """
        
        if not nome or len(nome.strip()) == 0:
            return None
        
        params = {
            "name": nome,
            "count": limite,
            "language": idioma
        }
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            if "results" in data:
                return data["results"]
            return None
        
        except requests.exceptions.Timeout:
            print(f"❌ Timeout ao buscar '{nome}'")
            return None
        
        except requests.exceptions.ConnectionError:
            print(f"❌ Erro de conexão ao buscar '{nome}'")
            return None
        
        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro HTTP: {e.response.status_code}")
            return None
        
        except Exception as e:
            print(f"❌ Erro ao buscar cidade: {str(e)}")
            return None
    
    def obter_melhor_resultado(self, nome: str) -> Optional[Dict]:
        """
        Retorna apenas o melhor resultado (primeiro da lista).
        Útil para quando você tem certeza do que está procurando.
        
        Args:
            nome: Nome da cidade
        
        Returns:
            Dicionário com nome, latitude, longitude, país, população, etc.
        
        Exemplo:
            cidade = obter_melhor_resultado("Brasília")
            print(f"{cidade['name']} - {cidade['country']}")
            # Brasília - Brasil
        """
        resultados = self.buscar_cidade(nome, limite=1)
        
        if resultados and len(resultados) > 0:
            return resultados[0]
        
        return None
    
    def extrair_coordenadas(self, nome: str) -> Optional[tuple]:
        """
        Retorna apenas as coordenadas (latitude, longitude) de uma cidade.
        
        Args:
            nome: Nome da cidade
        
        Returns:
            Tupla (latitude, longitude) ou None
        
        Exemplo:
            lat, lon = extrair_coordenadas("Brasília")
            print(lat, lon)  # -15.78 -47.89
        """
        cidade = self.obter_melhor_resultado(nome)
        
        if cidade:
            return (cidade.get("latitude"), cidade.get("longitude"))
        
        return None


# Função auxiliar (para uso simples, sem classe)
def buscar(nome: str, limite: int = 5) -> Optional[List[Dict]]:
    """
    Função simples para buscar cidades.
    
    Uso: cidades = buscar("São Paulo")
    """
    client = GeocodingClient()
    return client.buscar_cidade(nome, limite)


def coordenadas(nome: str) -> Optional[tuple]:
    """
    Função simples para obter apenas as coordenadas.
    
    Uso: lat, lon = coordenadas("Rio de Janeiro")
    """
    client = GeocodingClient()
    return client.extrair_coordenadas(nome)
