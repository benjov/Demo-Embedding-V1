"""
branding.py — identidad visual centralizada

Fuente: Manual de Identidad Corporativa de Analítica Boutique.

Paleta oficial:
 · #3C4981  azul corporativo  (Pantone 280 U)
 · #EE7F4B  naranja acento    (Pantone 158 U) — "el punto"

Tipografías:
 · Century Gothic — títulos y textos cortos de señalización
 · Calibri        — cuerpo de texto (impreso y digital)

Regla de uso del punto naranja: es un elemento gráfico que puede
aparecer como cierre de título, separador o marcador de atención.
"""

import streamlit as st


# ====================================================================
# PALETA
# ====================================================================
AB_BLUE = "#3C4981"          # Pantone 280 U — color dominante
AB_ORANGE = "#EE7F4B"        # Pantone 158 U — el punto

# Tintes y tonos derivados (todos del mismo matiz que el azul corporativo,
# respetando la regla del manual sobre conservar el matiz).
AB_BLUE_DARK = "#2d3660"
AB_BLUE_MID = "#5a6699"
AB_BLUE_SOFT = "#8a94bc"
AB_BLUE_PALE = "#d6dae8"
AB_BLUE_MIST = "#eef0f6"

# Naranja — tintes derivados
AB_ORANGE_DARK = "#c76332"
AB_ORANGE_SOFT = "#f6b088"

# Neutros
AB_WHITE = "#ffffff"
AB_INK = "#1f2544"          # texto principal, variante más oscura del azul
AB_GRAY = "#6b7285"          # texto secundario


# ====================================================================
# LOGO SVG
# ====================================================================
# Reproducción del logotipo corto de la marca (las letras "a" y "b"
# entrelazadas con el punto naranja). Ver manual, sección 1.a y 1.d.
LOGO_SVG = f"""
<div style="padding: 16px 0 4px 0;">
<svg viewBox="0 0 190 220" xmlns="http://www.w3.org/2000/svg"
     style="width: 110px; height: auto; display: block; margin: 0 auto;">
  <!-- "b" arriba -->
  <circle cx="62" cy="80" r="52" fill="none" stroke="{AB_BLUE}" stroke-width="14"/>
  <rect x="5" y="12" width="14" height="120" fill="{AB_BLUE}"/>
  <!-- "a" abajo -->
  <circle cx="128" cy="140" r="52" fill="none" stroke="{AB_BLUE}" stroke-width="14"/>
  <rect x="171" y="88" width="14" height="120" fill="{AB_BLUE}"/>
  <!-- el punto naranja en la intersección -->
  <circle cx="95" cy="110" r="13" fill="{AB_ORANGE}"/>
</svg>
<p style="text-align: center; font-family: 'Century Gothic', 'Questrial', sans-serif;
          color: {AB_BLUE}; font-weight: 400; letter-spacing: 0.5px;
          margin: 6px 0 0 0; font-size: 0.95rem; line-height: 1.15;">
  an<span style="color: {AB_ORANGE};">●</span>lítica<br/>boutique
</p>
</div>
"""


# ====================================================================
# CSS GLOBAL
# ====================================================================
def inject_css():
    """Inyecta la hoja de estilos global respetando el manual."""
    st.markdown(f"""
    <style>
    /* --- FUENTES ---
       Century Gothic y Calibri no son web-safe universales; usamos
       fuentes de Google muy cercanas como respaldo:
       Century Gothic → Questrial (mismo trazo geométrico)
       Calibri        → Lato        (humanista, muy cercano métricamente)
    */
    @import url('https://fonts.googleapis.com/css2?family=Questrial&family=Lato:wght@300;400;500;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, li, span, div,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
        font-family: 'Calibri', 'Lato', 'Segoe UI', sans-serif !important;
    }}
    h1, h2, h3, h4, h5, h6,
    .ab-h1, .ab-h2, .ab-h3,
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Century Gothic', 'Questrial', 'Segoe UI', sans-serif !important;
        font-weight: 400 !important;
        color: {AB_BLUE};
        letter-spacing: 0.2px;
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* --- CABECERA PRINCIPAL --- */
    .ab-h1 {{
        font-size: 2.2rem !important;
        font-weight: 400 !important;
        color: {AB_BLUE} !important;
        text-transform: lowercase;
        margin-bottom: 0.2rem !important;
        line-height: 1.15;
    }}
    .ab-subtitle {{
        color: {AB_GRAY};
        font-size: 1.05rem;
        font-style: italic;
        margin-top: -4px;
        margin-bottom: 1.2rem;
    }}
    .ab-dot, .ab-dot-letter .ab-dot {{
        color: {AB_ORANGE};
        font-weight: 700;
    }}

    /* --- SEPARADOR DE SECCIÓN, ESTILO MANUAL ---
       El manual usa una línea horizontal azul que termina en un
       punto naranja. Replicamos con un pseudo-elemento. */
    .ab-section {{
        position: relative;
        padding-bottom: 10px;
        margin: 1.6rem 0 1rem 0;
    }}
    .ab-section h2 {{
        font-family: 'Century Gothic', 'Questrial', sans-serif !important;
        color: {AB_BLUE} !important;
        font-size: 1.5rem !important;
        font-weight: 400 !important;
        text-transform: lowercase;
        margin: 0 0 6px 0 !important;
        padding-bottom: 6px !important;
    }}
    .ab-section::after {{
        content: "";
        display: block;
        height: 2px;
        background: linear-gradient(to right, {AB_BLUE_SOFT} 0%, {AB_BLUE} 85%, {AB_ORANGE} 100%);
        width: 100%;
        position: relative;
    }}
    .ab-section .ab-end-dot {{
        position: absolute;
        right: -4px;
        bottom: 2px;
        width: 10px;
        height: 10px;
        background: {AB_ORANGE};
        border-radius: 50%;
    }}

    /* --- SIDEBAR (fondo azul corporativo: regla del negativo) --- */
    [data-testid="stSidebar"] {{
        background-color: {AB_BLUE} !important;
    }}
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] li {{
        color: {AB_WHITE} !important;
    }}
    .ab-tagline {{
        font-family: 'Century Gothic', 'Questrial', sans-serif !important;
        font-size: 0.85rem;
        text-align: center;
        color: {AB_WHITE} !important;
        margin: 4px 0 10px 0;
        line-height: 1.25;
        letter-spacing: 0.3px;
    }}
    .ab-sidebar-label {{
        font-family: 'Century Gothic', 'Questrial', sans-serif !important;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: {AB_ORANGE} !important;
        margin: 0 0 4px 0;
    }}
    .ab-sidebar-value {{
        font-family: 'Calibri', 'Lato', sans-serif !important;
        font-weight: 700;
        font-size: 0.95rem;
        color: {AB_WHITE} !important;
        margin: 0 0 2px 0;
    }}
    .ab-sidebar-muted {{
        font-size: 0.8rem;
        color: rgba(255,255,255,0.65) !important;
        margin: 0;
        line-height: 1.4;
    }}
    .ab-toc {{
        font-family: 'Calibri', 'Lato', sans-serif !important;
        font-size: 0.88rem;
        color: rgba(255,255,255,0.85) !important;
        padding-left: 18px;
        margin: 0;
    }}
    .ab-toc li {{ margin-bottom: 3px; }}
    .ab-hr {{
        border: none;
        border-top: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
    }}

    /* --- TABS ---
       Replican el estilo del manual: título con línea degradada + punto naranja */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        border-bottom: 1px solid {AB_BLUE_PALE};
    }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 0.92rem;
        padding: 12px 18px;
        background-color: transparent;
        color: {AB_BLUE_MID} !important;
        text-transform: lowercase;
        font-weight: 400;
    }}
    .stTabs [aria-selected="true"] {{
        color: {AB_BLUE} !important;
        border-bottom: 2px solid {AB_ORANGE} !important;
        font-weight: 700;
    }}

    /* --- CAJAS DE INSIGHT --- */
    .insight-box {{
        background: {AB_BLUE_MIST};
        border-left: 3px solid {AB_BLUE};
        padding: 1.1rem 1.3rem;
        border-radius: 2px;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.55;
        color: {AB_INK};
    }}
    .warn-box {{
        background: #fdf3ec;
        border-left: 3px solid {AB_ORANGE};
        padding: 1.1rem 1.3rem;
        border-radius: 2px;
        margin: 1rem 0;
        color: {AB_INK};
    }}
    .warn-box b {{ color: {AB_ORANGE_DARK}; }}

    /* --- MÉTRICAS --- */
    [data-testid="stMetricValue"] {{
        font-family: 'Century Gothic', 'Questrial', sans-serif !important;
        color: {AB_BLUE} !important;
        font-weight: 400 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {AB_GRAY} !important;
        font-size: 0.82rem !important;
    }}

    /* --- FOOTER --- */
    .ab-footer {{
        text-align: center;
        color: {AB_GRAY};
        font-size: 0.82rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid {AB_BLUE_PALE};
    }}

    /* --- UTIL: punto naranja inline --- */
    .ab-bullet {{
        color: {AB_ORANGE};
        font-weight: 700;
        margin: 0 4px;
    }}

    /* --- TABLAS / DATAFRAMES --- */
    [data-testid="stDataFrame"] {{
        font-family: 'Calibri', 'Lato', sans-serif !important;
    }}

    /* --- INPUTS --- */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {{
        border-color: {AB_BLUE_PALE} !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {AB_ORANGE} !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ====================================================================
# HELPER: separador de sección estilo manual
# ====================================================================
def ab_section(title: str):
    """Renderiza un encabezado H2 con línea degradada + punto naranja."""
    st.markdown(
        f'<div class="ab-section"><h2>{title}</h2><span class="ab-end-dot"></span></div>',
        unsafe_allow_html=True,
    )
