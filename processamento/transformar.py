"""
transformar.py - Limpeza e transformação de dados climáticos

Módulo que converte dados brutos da API Open-Meteo em DataFrames pandas
organizados e prontos para visualização e análise.
"""

import pandas as pd
from typing import Dict, Optional
from datetime import datetime


class ProcessadorClima:
    """Processa e transforma dados climáticos da Open-Meteo API"""
    
    @staticmethod
    def processar_dados_horarios(dados_api: Dict) -> Optional[pd.DataFrame]:
        """
        Converte dados horários da API em DataFrame pandas.
        
        Args:
            dados_api: Resposta JSON da Open-Meteo Forecast API
        
        Returns:
            DataFrame com colunas: data_hora, temperatura, chuva, vento, umidade
        """
        
        if not dados_api or "hourly" not in dados_api:
            return None
        
        hourly = dados_api["hourly"]
        
        try:
            df = pd.DataFrame({
                "data_hora": pd.to_datetime(hourly["time"]),
                "temperatura": hourly["temperature_2m"],
                "precipitacao": hourly["precipitation"],
                "velocidade_vento": hourly["windspeed_10m"],
                "umidade": hourly["relativehumidity_2m"]
            })
            
            # Arredondar valores
            df["temperatura"] = df["temperatura"].round(1)
            df["velocidade_vento"] = df["velocidade_vento"].round(1)
            df["precipitacao"] = df["precipitacao"].round(1)
            
            return df
        
        except Exception as e:
            print(f"❌ Erro ao processar dados horários: {str(e)}")
            return None
    
    @staticmethod
    def processar_dados_diarios(dados_api: Dict) -> Optional[pd.DataFrame]:
        """
        Converte dados diários da API em DataFrame pandas.
        
        Args:
            dados_api: Resposta JSON da Open-Meteo Forecast API
        
        Returns:
            DataFrame com colunas: data, temp_max, temp_min, chuva_acumulada, vento_max
        """
        
        if not dados_api or "daily" not in dados_api:
            return None
        
        daily = dados_api["daily"]
        
        try:
            df = pd.DataFrame({
                "data": pd.to_datetime(daily["time"]),
                "temp_max": daily["temperature_2m_max"],
                "temp_min": daily["temperature_2m_min"],
                "precipitacao_acumulada": daily["precipitation_sum"],
                "velocidade_vento_max": daily["windspeed_10m_max"]
            })
            
            # Arredondar valores
            for col in df.columns:
                if col != "data":
                    df[col] = df[col].round(1)
            
            return df
        
        except Exception as e:
            print(f"❌ Erro ao processar dados diários: {str(e)}")
            return None
    
    @staticmethod
    def obter_resumo_diario(df_horarios: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Cria um resumo diário a partir dos dados horários.
        Calcula: temperatura média, min, max, chuva total, vento máximo.
        
        Args:
            df_horarios: DataFrame com dados horários
        
        Returns:
            DataFrame com resumo diário
        """
        
        if df_horarios is None or df_horarios.empty:
            return None
        
        try:
            # Extrair apenas a data (sem hora)
            df = df_horarios.copy()
            df["data"] = df["data_hora"].dt.date
            
            resumo = df.groupby("data").agg({
                "temperatura": ["min", "mean", "max"],
                "precipitacao": "sum",
                "velocidade_vento": "max",
                "umidade": "mean"
            }).round(1)
            
            # Achatar nomes das colunas
            resumo.columns = [
                "temp_min", "temp_media", "temp_max",
                "precipitacao_total", "vento_max", "umidade_media"
            ]
            
            return resumo.reset_index()
        
        except Exception as e:
            print(f"❌ Erro ao gerar resumo diário: {str(e)}")
            return None
    
    @staticmethod
    def obter_proximas_24h(df_horarios: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Retorna apenas as próximas 24 horas de dados.
        
        Args:
            df_horarios: DataFrame com dados horários
        
        Returns:
            DataFrame com 24 linhas (1 por hora)
        """
        
        if df_horarios is None or df_horarios.empty:
            return None
        
        try:
            return df_horarios.iloc[:24].copy()
        
        except Exception as e:
            print(f"❌ Erro ao extrair 24h: {str(e)}")
            return None
    
    @staticmethod
    def adicionar_fuso_horario(df: pd.DataFrame, timezone: str) -> pd.DataFrame:
        """
        Adiciona informação de fuso horário aos dados.
        
        Args:
            df: DataFrame com coluna de data/hora
            timezone: Fuso horário (ex: "America/Sao_Paulo")
        
        Returns:
            DataFrame com coluna de timezone adicionada
        """
        
        df = df.copy()
        df["fuso_horario"] = timezone
        return df


# Funções auxiliares (para uso simples, sem classe)

def processar_api(dados_api: Dict) -> tuple:
    """
    Processa dados da API e retorna (df_horarios, df_diarios, timezone).
    
    Uso: horarios, diarios, tz = processar_api(dados)
    """
    processador = ProcessadorClima()
    
    df_horarios = processador.processar_dados_horarios(dados_api)
    df_diarios = processador.processar_dados_diarios(dados_api)
    timezone = dados_api.get("timezone", "UTC")
    
    return df_horarios, df_diarios, timezone


def resumo_24h(df_horarios: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Retorna resumo dos próximos 7 dias a partir dos dados horários.
    
    Uso: resumo = resumo_24h(df_horarios)
    """
    processador = ProcessadorClima()
    return processador.obter_resumo_diario(df_horarios)
