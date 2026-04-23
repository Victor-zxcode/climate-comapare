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
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main { padding: 0rem 1rem; }
        h1 { text-align: center; margin-bottom: 2rem; }
        .metric-card { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
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


st.markdown("# 🌍 Climate Compare")
st.markdown("**Visualize e compare dados climáticos de qualquer lugar do mundo**")
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    busca_tipo = st.radio(
        "Selecione uma opção:",
        ["📍 Buscar por cidade", "⭐ Capitais pré-carregadas"],
        horizontal=True
    )

with col2:
    max_cidades = st.number_input("Máximo de cidades:", min_value=1, max_value=5, value=3)

st.divider()

cidades_selecionadas = []

if busca_tipo == "📍 Buscar por cidade":
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        busca = st.text_input("Digite o nome de uma cidade ou país:")
    
    with col2:
        buscar_btn = st.button("🔍 Buscar", use_container_width=True)
    
    if buscar_btn and busca:
        with st.spinner("Buscando cidades..."):
            resultados = fetch_city_search(busca)
        
        if resultados:
            st.subheader("Resultados encontrados:")
            
            cols = st.columns(min(len(resultados), 3))
            for idx, resultado in enumerate(resultados[:3]):
                with cols[idx]:
                    if st.button(
                        f"✓ {resultado['name']}\n{resultado['country']}",
                        key=f"result_{idx}",
                        use_container_width=True
                    ):
                        st.session_state[f"selected_{idx}"] = resultado
        else:
            st.warning("Nenhuma cidade encontrada. Tente outro nome.")

else:
    capitais = listar_nomes()
    cols = st.columns(2)
    
    for i in range(max_cidades):
        with cols[i % 2]:
            capital = st.selectbox(
                f"Capital {i+1}:",
                capitais,
                key=f"capital_{i}"
            )
            if capital:
                info = obter_info_completa(capital)
                st.session_state[f"selected_{i}"] = {
                    "name": info["nome"],
                    "country": info["pais"],
                    "latitude": info["latitude"],
                    "longitude": info["longitude"]
                }


for i in range(max_cidades):
    if f"selected_{i}" in st.session_state:
        cidade = st.session_state[f"selected_{i}"]
        cidades_selecionadas.append(cidade)

st.divider()

if cidades_selecionadas:
    st.subheader(f"📊 Dados climáticos de {len(cidades_selecionadas)} local(is)")
    
    dados_por_cidade = {}
    
    with st.spinner("Carregando dados climáticos..."):
        for cidade in cidades_selecionadas:
            dados = fetch_weather(cidade["latitude"], cidade["longitude"])
            if dados:
                processador = ProcessadorClima()
                df_horarios, df_diarios, tz = processar_api(dados)
                dados_por_cidade[cidade["name"]] = {
                    "horarios": df_horarios,
                    "diarios": df_diarios,
                    "timezone": tz,
                    "latitude": cidade["latitude"],
                    "longitude": cidade["longitude"],
                    "pais": cidade["country"]
                }
    
    if dados_por_cidade:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Temperatura",
            "💧 Precipitação",
            "💨 Vento",
            "📋 Comparativo"
        ])
        
        with tab1:
            fig = go.Figure()
            
            for nome, dados in dados_por_cidade.items():
                df = dados["diarios"].copy()
                df["temp_media"] = (df["temp_max"] + df["temp_min"]) / 2
                
                fig.add_trace(go.Scatter(
                    x=df["data"],
                    y=df["temp_media"],
                    name=f"{nome} (média)",
                    mode="lines+markers",
                    line=dict(width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=df["data"],
                    y=df["temp_max"],
                    name=f"{nome} (máx)",
                    mode="lines",
                    line=dict(width=1, dash="dash")
                ))
                
                fig.add_trace(go.Scatter(
                    x=df["data"],
                    y=df["temp_min"],
                    name=f"{nome} (mín)",
                    mode="lines",
                    line=dict(width=1, dash="dash"),
                    fill="tonexty"
                ))
            
            fig.update_layout(
                title="Temperatura (7 dias)",
                xaxis_title="Data",
                yaxis_title="Temperatura (°C)",
                hovermode="x unified",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = go.Figure()
            
            for nome, dados in dados_por_cidade.items():
                df = dados["diarios"]
                fig.add_trace(go.Bar(
                    x=df["data"],
                    y=df["precipitacao_acumulada"],
                    name=nome,
                    opacity=0.7
                ))
            
            fig.update_layout(
                title="Precipitação Acumulada (7 dias)",
                xaxis_title="Data",
                yaxis_title="Precipitação (mm)",
                barmode="group",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = go.Figure()
            
            for nome, dados in dados_por_cidade.items():
                df = dados["diarios"]
                fig.add_trace(go.Scatter(
                    x=df["data"],
                    y=df["velocidade_vento_max"],
                    name=nome,
                    mode="lines+markers",
                    line=dict(width=3)
                ))
            
            fig.update_layout(
                title="Velocidade Máxima do Vento (7 dias)",
                xaxis_title="Data",
                yaxis_title="Velocidade (km/h)",
                hovermode="x unified",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("Comparativo - Próximas 24 horas")
            
            col1, col2, col3 = st.columns(len(cidades_selecionadas))
            cols_list = [col1, col2, col3]
            
            for idx, (nome, dados) in enumerate(dados_por_cidade.items()):
                with cols_list[idx]:
                    df_24h = dados["horarios"].iloc[:24]
                    
                    st.markdown(f"### {nome}")
                    st.markdown(f"**País:** {dados['pais']}")
                    
                    st.metric(
                        "🌡 Temperatura",
                        f"{df_24h['temperatura'].iloc[0]:.1f}°C",
                        f"{df_24h['temperatura'].mean():.1f}° média"
                    )
                    
                    st.metric(
                        "💧 Umidade",
                        f"{df_24h['umidade'].iloc[0]:.0f}%",
                        f"{df_24h['umidade'].mean():.0f}% média"
                    )
                    
                    st.metric(
                        "💨 Vento",
                        f"{df_24h['velocidade_vento'].iloc[0]:.1f} km/h",
                        f"{df_24h['velocidade_vento'].max():.1f} km/h máx"
                    )
                    
                    st.metric(
                        "🌧 Chuva",
                        f"{df_24h['precipitacao'].sum():.1f}mm",
                        "próximas 24h"
                    )
        
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("📥 Exportar dados em CSV", use_container_width=True):
                dfs_export = []
                
                for nome, dados in dados_por_cidade.items():
                    df = dados["diarios"].copy()
                    df["cidade"] = nome
                    dfs_export.append(df)
                
                df_export = pd.concat(dfs_export, ignore_index=True)
                csv = df_export.to_csv(index=False)
                
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"climate_compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
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

