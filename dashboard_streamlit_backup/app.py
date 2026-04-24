import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from coleta.api_client import OpenMeteoClient
from coleta.geocoding import GeocodingClient
from processamento.transformar import ProcessadorClima, processar_api
from utils.capitais import listar_nomes, obter_coordenadas, obter_info_completa


st.set_page_config(
    page_title="Climate Compare",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        * { margin: 0; padding: 0; }
        .main { 
            padding: 2rem 2rem !important;
            background-color: #f8f9fa;
        }
        
        .header {
            text-align: left;
            margin-bottom: 0.5rem;
        }
        
        .header-title {
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a1a;
            margin: 0;
        }
        
        .header-subtitle {
            font-size: 0.9rem;
            color: #999;
            margin: 0;
        }
        
        .search-container {
            margin: 2rem 0;
            position: relative;
        }
        
        .search-input {
            width: 100%;
            padding: 1rem;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            background: white;
        }
        
        .chip-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1rem 0;
            align-items: center;
        }
        
        .chip {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            font-size: 0.9rem;
            color: #333;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .chip-close {
            cursor: pointer;
            font-weight: bold;
            color: #999;
        }
        
        .chip-close:hover {
            color: #333;
        }
        
        .add-city-btn {
            padding: 0.5rem 1rem;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            color: #666;
            transition: all 0.3s ease;
        }
        
        .add-city-btn:hover {
            background-color: #e8e8e8;
            border-color: #999;
        }
        
        .temp-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #f0f0f0;
            transition: box-shadow 0.3s ease;
        }
        
        .temp-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        .temp-card-header {
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }
        
        .temp-card-subheader {
            color: #999;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }
        
        .temp-value {
            font-size: 3rem;
            font-weight: 700;
            color: #1a1a1a;
            margin: 0.5rem 0;
        }
        
        .temp-description {
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }
        
        .weather-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #f0f0f0;
        }
        
        .weather-item {
            text-align: center;
            padding: 0.5rem 0;
        }
        
        .weather-label {
            font-size: 0.75rem;
            color: #999;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
        }
        
        .weather-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
        }
        
        .chart-container {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #f0f0f0;
        }
        
        .chart-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 1rem;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #f0f0f0;
        }
        
        .metric-card-title {
            font-size: 0.85rem;
            color: #999;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }
        
        .metric-bar-container {
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
        }
        
        .metric-bar-label {
            font-size: 0.9rem;
            color: #333;
            font-weight: 500;
            width: 60px;
            flex-shrink: 0;
        }
        
        .metric-bar {
            flex: 1;
            height: 8px;
            background-color: #f0f0f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 0.5rem;
        }
        
        .metric-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }
        
        .metric-bar-value {
            font-size: 0.9rem;
            color: #666;
            width: 40px;
            text-align: right;
        }
        
        .wind-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            align-items: center;
        }
        
        .wind-speed {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .wind-direction {
            font-size: 1.1rem;
            color: #999;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_clients():
    return OpenMeteoClient(), GeocodingClient()

@st.cache_data(ttl=3600)
def fetch_weather(lat, lon):
    client, _ = get_clients()
    return client.obter_previsao(lat, lon)

@st.cache_data(ttl=3600)
def fetch_city_search(nome):
    _, geo = get_clients()
    return geo.buscar_cidade(nome, limite=5)

def obter_descricao_clima(condition_code):
    """Retorna descrição do clima baseado no código"""
    descricoes = {
        0: "Céu limpo",
        1: "Parcialmente nublado",
        2: "Nublado",
        3: "Encoberto",
        45: "Nevoeiro",
        48: "Nevoeiro com deposição de gelo",
        51: "Chuvisco leve",
        53: "Chuvisco moderado",
        55: "Chuvisco denso",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva forte",
        71: "Neve leve",
        73: "Neve moderada",
        75: "Neve forte",
        77: "Grãos de neve",
        80: "Pancadas de chuva leve",
        81: "Pancadas de chuva moderada",
        82: "Pancadas de chuva forte",
        85: "Pancadas de neve leve",
        86: "Pancadas de neve forte",
        95: "Tempestade com raios leves",
        96: "Tempestade com raios moderados",
        99: "Tempestade com raios fortes",
    }
    return descricoes.get(condition_code, "Sem informação")

def obter_direcao_vento(graus):
    """Converte graus em direção do vento"""
    direcoes = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(graus / 22.5) % 16
    return direcoes[idx]

# Inicializar session state
if "cidades" not in st.session_state:
    st.session_state.cidades = []

if "busca_input" not in st.session_state:
    st.session_state.busca_input = ""

if "resultados_busca" not in st.session_state:
    st.session_state.resultados_busca = []

# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.markdown('<h1 class="header-title">🌍 Climate Compare</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">/ mundial</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Barra de busca
col_search = st.container()
with col_search:
    busca = st.text_input(
        "Buscar cidade, capital, país",
        placeholder="Digite aqui...",
        key="search_input",
        label_visibility="collapsed"
    )

# Processar busca
if busca and busca != st.session_state.get("last_search", ""):
    st.session_state.last_search = busca
    with st.spinner("Buscando cidades..."):
        resultados = fetch_city_search(busca)
        st.session_state.resultados_busca = resultados if resultados else []

# Mostrar resultados de busca
if st.session_state.resultados_busca and busca:
    st.markdown("### Resultados encontrados:")
    cols = st.columns(min(len(st.session_state.resultados_busca), 3))
    
    for idx, resultado in enumerate(st.session_state.resultados_busca[:3]):
        with cols[idx]:
            if st.button(
                f"✓ {resultado['name']}\n{resultado['country']}",
                key=f"result_btn_{idx}",
                use_container_width=True
            ):
                nova_cidade = {
                    "name": resultado['name'],
                    "country": resultado['country'],
                    "latitude": resultado['latitude'],
                    "longitude": resultado['longitude']
                }
                if nova_cidade not in st.session_state.cidades:
                    st.session_state.cidades.append(nova_cidade)
                st.session_state.resultados_busca = []
                st.rerun()

# Mostrar chips com cidades selecionadas
if st.session_state.cidades:
    st.markdown('<div class="chip-container">', unsafe_allow_html=True)
    
    cols_chips = st.columns(len(st.session_state.cidades) + 1)
    
    for idx, cidade in enumerate(st.session_state.cidades):
        with cols_chips[idx]:
            col_chip_remove, col_chip_text = st.columns([0.1, 0.9])
            
            with col_chip_remove:
                if st.button("✕", key=f"remove_{idx}", help="Remover"):
                    st.session_state.cidades.pop(idx)
                    st.rerun()
            
            with col_chip_text:
                pais_code = cidade.get("country", "").split(",")[-1].strip()[:2] if "," in cidade.get("country", "") else ""
                st.markdown(f'<span style="font-weight: 500;">{cidade["name"]}</span> <span style="color: #999;">{pais_code}</span>', unsafe_allow_html=True)
    
    with cols_chips[-1]:
        if st.button("+ adicionar local", key="add_city"):
            pass
    
    st.markdown('</div>', unsafe_allow_html=True)

cidades_selecionadas = st.session_state.cidades

if cidades_selecionadas:
    dados_por_cidade = {}
    
    with st.spinner("Carregando dados climáticos..."):
        for cidade in cidades_selecionadas:
            dados = fetch_weather(cidade["latitude"], cidade["longitude"])
            if dados:
                processador = ProcessadorClima()
                df_horarios, df_diarios, tz = processar_api(dados)
                
                # Obter dados adicionais da primeira hora
                current_temp = df_horarios.iloc[0] if len(df_horarios) > 0 else None
                
                # Tentar obter código de clima (pode não existir em todas as respostas)
                weather_code = 0
                if "hourly" in dados and "weather_code" in dados.get("hourly", {}):
                    weather_codes = dados["hourly"]["weather_code"]
                    weather_code = weather_codes[0] if isinstance(weather_codes, list) and len(weather_codes) > 0 else 0
                
                # Obter direção do vento
                wind_direction = "N"
                if "hourly" in dados and "wind_direction_10m" in dados.get("hourly", {}):
                    wind_dirs = dados["hourly"]["wind_direction_10m"]
                    if isinstance(wind_dirs, list) and len(wind_dirs) > 0:
                        wind_direction = obter_direcao_vento(wind_dirs[0])
                
                dados_por_cidade[cidade["name"]] = {
                    "horarios": df_horarios,
                    "diarios": df_diarios,
                    "timezone": tz,
                    "latitude": cidade["latitude"],
                    "longitude": cidade["longitude"],
                    "pais": cidade["country"],
                    "weather_code": weather_code,
                    "wind_direction": wind_direction,
                    "raw_data": dados
                }
    
    if dados_por_cidade:
        # ========== CARDS DE TEMPERATURA ==========
        st.markdown("<br>", unsafe_allow_html=True)
        
        cols = st.columns(len(cidades_selecionadas))
        
        for idx, (nome, dados) in enumerate(dados_por_cidade.items()):
            with cols[idx]:
                df_24h = dados["horarios"].iloc[:24] if len(dados["horarios"]) >= 24 else dados["horarios"]
                
                temp_atual = df_24h['temperatura'].iloc[0]
                umidade = df_24h['umidade'].iloc[0]
                chuva = df_24h['precipitacao'].sum()
                vento = df_24h['velocidade_vento'].iloc[0]
                descricao = obter_descricao_clima(dados["weather_code"])
                
                pais_tz = dados["pais"].split(",")
                pais = pais_tz[0].strip() if pais_tz else "Desconhecido"
                tz_str = pais_tz[1].strip() if len(pais_tz) > 1 else dados["timezone"]
                
                st.markdown(f"""
                <div class="temp-card">
                    <div class="temp-card-header">{nome}</div>
                    <div class="temp-card-subheader">{pais} • {tz_str}</div>
                    <div class="temp-value">{temp_atual:.0f}°C</div>
                    <div class="temp-description">{descricao}</div>
                    <div class="weather-grid">
                        <div class="weather-item">
                            <div class="weather-label">Chuva</div>
                            <div class="weather-value">{chuva:.1f} mm</div>
                        </div>
                        <div class="weather-item">
                            <div class="weather-label">Umidade</div>
                            <div class="weather-value">{umidade:.0f}%</div>
                        </div>
                        <div class="weather-item">
                            <div class="weather-label">Vento</div>
                            <div class="weather-value">{vento:.1f} km/h</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # ========== GRÁFICO DE TEMPERATURA ==========
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Temperatura — próximos 7 dias</div>', unsafe_allow_html=True)
        
        fig = go.Figure()
        colors = ["#4f46e5", "#059669", "#dc2626", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4"]
        
        for idx, (nome, dados) in enumerate(dados_por_cidade.items()):
            df = dados["diarios"].copy()
            df["temp_media"] = (df["temp_max"] + df["temp_min"]) / 2
            
            fig.add_trace(go.Scatter(
                x=df["data"],
                y=df["temp_media"],
                name=nome,
                mode="lines",
                line=dict(color=colors[idx % len(colors)], width=3),
                hovertemplate="<b>" + nome + "</b><br>%{x}<br>%{y:.1f}°C<extra></extra>"
            ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12, color="#666"),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor="#f0f0f0",
                showline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor="#f0f0f0",
                showline=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ========== CARDS DE PRECIPITAÇÃO E VENTO ==========
        st.markdown("<br>", unsafe_allow_html=True)
        
        cols_metrics = st.columns(2)
        
        with cols_metrics[0]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">💧 Precipitação Acum. (mm)</div>', unsafe_allow_html=True)
            
            for nome, dados in dados_por_cidade.items():
                df = dados["diarios"]
                precip_total = df["precipitacao_acumulada"].iloc[0]
                
                st.markdown(f"""
                <div class="metric-bar-container">
                    <div class="metric-bar-label">{nome}</div>
                    <div class="metric-bar">
                        <div class="metric-bar-fill" style="width: {min(precip_total / max(df['precipitacao_acumulada'].max(), 50) * 100, 100)}%"></div>
                    </div>
                    <div class="metric-bar-value">{precip_total:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with cols_metrics[1]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">💨 Velocidade do Vento</div>', unsafe_allow_html=True)
            
            for nome, dados in dados_por_cidade.items():
                df = dados["diarios"]
                vento_max = df["velocidade_vento_max"].iloc[0]
                wind_dir = dados.get("wind_direction", "N")
                
                st.markdown(f"""
                <div style="margin-bottom: 1.5rem;">
                    <div style="font-size: 0.9rem; color: #333; font-weight: 500; margin-bottom: 0.5rem;">{nome}</div>
                    <div class="wind-section">
                        <div>
                            <div class="wind-speed">{vento_max:.0f}</div>
                            <div style="color: #999; font-size: 0.9rem;">km/h</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="wind-direction">{wind_dir}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ========== GRÁFICOS ADICIONAIS ==========
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_tabs = st.container()
        with col_tabs:
            tab1, tab2 = st.tabs(["📈 Precipitação (7 dias)", "💨 Vento (7 dias)"])
            
            with tab1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                fig_precip = go.Figure()
                
                for idx, (nome, dados) in enumerate(dados_por_cidade.items()):
                    df = dados["diarios"]
                    fig_precip.add_trace(go.Bar(
                        x=df["data"],
                        y=df["precipitacao_acumulada"],
                        name=nome,
                        marker=dict(color=colors[idx % len(colors)]),
                        opacity=0.8,
                        hovertemplate="<b>" + nome + "</b><br>%{x}<br>%{y:.1f}mm<extra></extra>"
                    ))
                
                fig_precip.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0),
                    barmode="group",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(size=12, color="#666"),
                    xaxis=dict(showgrid=False, showline=False),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#f0f0f0", showline=False),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig_precip, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                fig_wind = go.Figure()
                
                for idx, (nome, dados) in enumerate(dados_por_cidade.items()):
                    df = dados["diarios"]
                    fig_wind.add_trace(go.Scatter(
                        x=df["data"],
                        y=df["velocidade_vento_max"],
                        name=nome,
                        mode="lines+markers",
                        line=dict(color=colors[idx % len(colors)], width=3),
                        hovertemplate="<b>" + nome + "</b><br>%{x}<br>%{y:.1f} km/h<extra></extra>"
                    ))
                
                fig_wind.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=0, b=0),
                    hovermode="x unified",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(size=12, color="#666"),
                    xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#f0f0f0", showline=False),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#f0f0f0", showline=False),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig_wind, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Busque uma cidade acima para começar a comparar dados climáticos!")
        
        with col2:
            st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")

else:
    st.info("👉 Selecione pelo menos uma cidade para começar!")

st.divider()

with st.expander("ℹ️ Sobre este projeto"):
    st.markdown("""
    **Climate Compare** é um dashboard interativo que coleta dados climáticos em tempo real
    de qualquer cidade do mundo usando a **Open-Meteo API**.
    
    ### Tecnologias
    - 🐍 Python + Streamlit
    - 📊 Pandas para processamento de dados
    - 📈 Plotly para gráficos interativos
    - 🌐 Open-Meteo API (dados climáticos gratuitos)
    
    ### Dados disponíveis
    - Previsão de 7 dias
    - Temperatura, precipitação, umidade e velocidade do vento
    - Comparação lado a lado de múltiplas cidades
    
    [Código no GitHub](https://github.com/Victor-zxcode/climate-comapare)
    """)

