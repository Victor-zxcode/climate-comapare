"""
capitais.py - Lista de capitais do mundo com coordenadas

Módulo que contém uma lista pré-carregada de capitais mundiais
para facilitar autocomplete e busca rápida sem chamar a API.
"""

# Dicionário com capitais do mundo: {nome_da_capital: (latitude, longitude, país)}
CAPITAIS_MUNDO = {
    # América do Norte
    "Washington": (38.89, -77.04, "Estados Unidos"),
    "Cidade do México": (19.43, -99.13, "México"),
    "Ottawa": (45.42, -75.70, "Canadá"),
    
    # América do Sul
    "Brasília": (-15.79, -47.88, "Brasil"),
    "Rio de Janeiro": (-22.91, -43.17, "Brasil"),
    "São Paulo": (-23.55, -46.63, "Brasil"),
    "Buenos Aires": (-34.61, -58.37, "Argentina"),
    "Lima": (-12.05, -77.04, "Peru"),
    "La Paz": (-16.50, -68.15, "Bolívia"),
    "Asunción": (-25.26, -57.57, "Paraguai"),
    "Monteveridéu": (-34.88, -56.17, "Uruguai"),
    "Caracas": (10.49, -66.86, "Venezuela"),
    "Bogotá": (4.71, -74.07, "Colômbia"),
    "Quito": (-0.22, -78.51, "Equador"),
    "Santiago": (-33.44, -70.67, "Chile"),
    
    # Europa
    "Lisboa": (38.72, -9.14, "Portugal"),
    "Madrid": (40.42, -3.70, "Espanha"),
    "Paris": (48.86, 2.35, "França"),
    "Londres": (51.51, -0.13, "Reino Unido"),
    "Dublin": (53.35, -6.26, "Irlanda"),
    "Berlim": (52.52, 13.40, "Alemanha"),
    "Amsterdã": (52.37, 4.89, "Holanda"),
    "Bruxelas": (50.85, 4.36, "Bélgica"),
    "Zurique": (47.37, 8.55, "Suíça"),
    "Viena": (48.21, 16.37, "Áustria"),
    "Praga": (50.08, 14.44, "República Tcheca"),
    "Varsóvia": (52.23, 21.01, "Polônia"),
    "Roma": (41.90, 12.50, "Itália"),
    "Atenas": (37.98, 23.73, "Grécia"),
    "Istambul": (41.01, 28.98, "Turquia"),
    "Moscou": (55.76, 37.62, "Rússia"),
    "Helsinque": (60.17, 24.94, "Finlândia"),
    "Estocolmo": (59.33, 18.07, "Suécia"),
    "Copenhague": (55.68, 12.57, "Dinamarca"),
    "Oslo": (59.91, 10.75, "Noruega"),
    "Belgrado": (44.82, 20.46, "Sérvia"),
    
    # Ásia
    "Tóquio": (35.68, 139.69, "Japão"),
    "Pequim": (39.90, 116.41, "China"),
    "Xangai": (31.23, 121.47, "China"),
    "Xian": (34.27, 108.95, "China"),
    "Seul": (37.57, 126.98, "Coreia do Sul"),
    "Bangkok": (13.73, 100.49, "Tailândia"),
    "Singapura": (1.35, 103.82, "Singapura"),
    "Kuala Lumpur": (3.14, 101.69, "Malásia"),
    "Jacarta": (-6.21, 106.85, "Indonésia"),
    "Hanói": (21.03, 105.85, "Vietnã"),
    "Phnom Penh": (11.56, 104.92, "Camboja"),
    "Manila": (14.60, 120.98, "Filipinas"),
    "Nova Délhi": (28.61, 77.23, "Índia"),
    "Mumbai": (19.08, 72.88, "Índia"),
    "Calcutá": (22.57, 88.36, "Índia"),
    "Karachi": (24.86, 67.01, "Paquistão"),
    "Islamabad": (33.73, 73.17, "Paquistão"),
    "Cabul": (34.53, 69.18, "Afeganistão"),
    "Teerã": (35.69, 51.39, "Irã"),
    "Bagdá": (33.31, 44.36, "Iraque"),
    "Damasco": (33.51, 36.28, "Síria"),
    "Beirute": (33.87, 35.50, "Líbano"),
    "Tel Aviv": (32.09, 34.78, "Israel"),
    "Amã": (31.95, 35.93, "Jordânia"),
    "Riad": (24.77, 46.67, "Arábia Saudita"),
    "Doha": (25.29, 51.53, "Qatar"),
    "Dubai": (25.27, 55.31, "Emirados Árabes Unidos"),
    "Abu Dhabi": (24.45, 54.37, "Emirados Árabes Unidos"),
    "Koweit": (29.38, 47.98, "Kuwait"),
    "Mascate": (23.61, 58.54, "Omã"),
    
    # África
    "Cairo": (30.05, 31.24, "Egito"),
    "Lagos": (6.52, 3.36, "Nigéria"),
    "Joanesburgo": (-26.20, 28.04, "África do Sul"),
    "Pretória": (-25.75, 28.23, "África do Sul"),
    "Adis Abeba": (9.03, 38.75, "Etiópia"),
    "Nairóbi": (-1.28, 36.82, "Quênia"),
    "Dar es Salaam": (-6.80, 39.27, "Tanzânia"),
    "Cartum": (15.50, 32.53, "Sudão"),
    "Casablanca": (33.57, -7.59, "Marrocos"),
    "Rabat": (34.02, -6.84, "Marrocos"),
    "Argel": (36.75, 3.06, "Argélia"),
    "Túnis": (36.81, 10.18, "Tunísia"),
    "Tripoli": (32.89, 13.19, "Líbia"),
    "Acra": (5.55, -0.19, "Gana"),
    "Abidjan": (5.33, -4.03, "Costa do Marfim"),
    "Dacar": (14.70, -17.04, "Senegal"),
    "Accra": (5.65, -0.16, "Gana"),
    
    # Oceania
    "Camberra": (-35.28, 149.13, "Austrália"),
    "Melbourne": (-37.81, 144.96, "Austrália"),
    "Sydney": (-33.87, 151.21, "Austrália"),
    "Auckland": (-37.01, 174.89, "Nova Zelândia"),
    "Suva": (-18.13, 178.44, "Fiji"),
    "Port Moresby": (-9.48, 147.18, "Papua-Nova Guiné"),
}


def obter_capitais() -> dict:
    """
    Retorna o dicionário completo de capitais.
    
    Returns:
        Dicionário com formato: {nome: (lat, lon, país)}
    """
    return CAPITAIS_MUNDO.copy()


def listar_nomes() -> list:
    """
    Retorna uma lista com os nomes de todas as capitais.
    Útil para autocomplete no dashboard.
    
    Returns:
        Lista de nomes de capitais ordenados alfabeticamente
    
    Uso: nomes = listar_nomes()
         # ["Abidjan", "Abu Dhabi", "Accra", ...]
    """
    return sorted(CAPITAIS_MUNDO.keys())


def obter_coordenadas(capital: str) -> tuple:
    """
    Retorna as coordenadas de uma capital.
    
    Args:
        capital: Nome da capital
    
    Returns:
        Tupla (latitude, longitude) ou (None, None) se não encontrada
    
    Uso: lat, lon = obter_coordenadas("Brasília")
    """
    if capital in CAPITAIS_MUNDO:
        lat, lon, _ = CAPITAIS_MUNDO[capital]
        return (lat, lon)
    return (None, None)


def obter_info_completa(capital: str) -> dict:
    """
    Retorna informações completas de uma capital.
    
    Args:
        capital: Nome da capital
    
    Returns:
        Dicionário com {nome, latitude, longitude, país} ou None
    
    Uso: info = obter_info_completa("Lisboa")
         # {"nome": "Lisboa", "latitude": 38.72, ...}
    """
    if capital in CAPITAIS_MUNDO:
        lat, lon, pais = CAPITAIS_MUNDO[capital]
        return {
            "nome": capital,
            "latitude": lat,
            "longitude": lon,
            "pais": pais
        }
    return None


def listar_por_pais(pais: str) -> list:
    """
    Retorna todas as capitais de um país.
    
    Args:
        pais: Nome do país
    
    Returns:
        Lista de capitais daquele país
    
    Uso: brasil = listar_por_pais("Brasil")
         # ["Brasília", "Rio de Janeiro", "São Paulo"]
    """
    return [
        capital for capital, (_, _, p) in CAPITAIS_MUNDO.items()
        if p.lower() == pais.lower()
    ]


def total_capitais() -> int:
    """
    Retorna o número total de capitais na lista.
    
    Uso: total = total_capitais()  # 143
    """
    return len(CAPITAIS_MUNDO)
