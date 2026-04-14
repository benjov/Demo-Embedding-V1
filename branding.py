"""
branding.py — identidad visual centralizada

Versión inspirada en el landing de analiticaboutique.com.mx:
fondo azul marino profundo con gradiente radial, tipografía grotesk
moderna, naranja como acento puntual (CTAs, highlights), no como
protagonista. Óptimo para proyectar en sala de juntas.

Paleta oficial (Manual de Identidad):
 · #3C4981  azul corporativo  (Pantone 280 U)
 · #EE7F4B  naranja acento    (Pantone 158 U)

Tipografías:
 · Headings: Manrope (grotesk moderna, cercana a la del landing)
 · Cuerpo:   Lato (fallback web de Calibri)
"""

import streamlit as st


# ====================================================================
# PALETA
# ====================================================================
AB_BLUE = "#3C4981"
AB_ORANGE = "#EE7F4B"

# Fondo sala de juntas — azul marino profundo con matiz del corporativo
AB_BG_DEEP = "#0B1230"
AB_BG = "#141b3d"
AB_BG_ELEV = "#1e2654"
AB_BG_GRAD = "#2a3268"

# Textos sobre fondo oscuro
AB_TEXT = "#ffffff"
AB_TEXT_SOFT = "#c5cadd"
AB_TEXT_MUTED = "#8790b0"

# Azul corporativo adaptado para legibilidad sobre fondo oscuro
AB_BLUE_BRIGHT = "#6d7ec0"
AB_BLUE_LIGHT = "#9aa6d6"
AB_BLUE_PALE = "#3b4470"

# Naranja (uso discreto)
AB_ORANGE_BRIGHT = "#f28b5c"
AB_ORANGE_DEEP = "#c76332"


# ====================================================================
# LOGO SVG para sidebar
# ====================================================================
LOGO_SVG = f"""
<div style="padding: 18px 0 6px 0;">
<svg viewBox="0 0 320 110" xmlns="http://www.w3.org/2000/svg"
     style="width: 185px; height: auto; display: block; margin: 0 auto;">
  <!-- letra b -->
  <g transform="translate(10, 12)">
    <circle cx="30" cy="50" r="28" fill="none" stroke="{AB_TEXT}" stroke-width="6"/>
    <rect x="-2" y="-2" width="6" height="82" fill="{AB_TEXT}"/>
  </g>
  <!-- letra a entrelazada -->
  <g transform="translate(46, 2)">
    <circle cx="30" cy="50" r="28" fill="none" stroke="{AB_TEXT}" stroke-width="6"/>
    <rect x="56" y="22" width="6" height="82" fill="{AB_TEXT}"/>
  </g>
  <!-- el punto naranja, discreto -->
  <circle cx="72" cy="56" r="6" fill="{AB_ORANGE}"/>
  <!-- wordmark -->
  <text x="128" y="50"
        font-family="Manrope, sans-serif"
        font-size="28" font-weight="500" fill="{AB_TEXT}"
        letter-spacing="-0.5">analítica</text>
  <text x="128" y="82"
        font-family="Manrope, sans-serif"
        font-size="28" font-weight="300" fill="{AB_TEXT}"
        letter-spacing="-0.5">boutique</text>
</svg>
</div>
"""


# ====================================================================
# CSS GLOBAL
# ====================================================================
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Lato:wght@300;400;500;700&display=swap');

    /* FONDO GLOBAL con gradiente radial al estilo landing */
    .stApp {{
        background:
            radial-gradient(ellipse 80% 60% at 20% 10%,
                            {AB_BG_GRAD} 0%,
                            {AB_BG} 45%,
                            {AB_BG_DEEP} 100%);
        background-attachment: fixed;
        color: {AB_TEXT};
    }}
    .block-container {{
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* TIPOGRAFÍA */
    html, body, [class*="css"], .stMarkdown, p, li, span, div,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
    .stTextInput input, .stSelectbox {{
        font-family: 'Lato', 'Calibri', 'Segoe UI', sans-serif !important;
        color: {AB_TEXT_SOFT};
    }}
    h1, h2, h3, h4, h5, h6,
    .ab-h1, .ab-h2, .ab-h3,
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Manrope', 'Questrial', sans-serif !important;
        color: {AB_TEXT} !important;
        letter-spacing: -0.015em;
    }}
    strong, b {{ color: {AB_TEXT}; font-weight: 600; }}

    /* CABECERA PRINCIPAL al estilo landing */
    .ab-h1 {{
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        color: {AB_TEXT} !important;
        margin-bottom: 0.4rem !important;
        line-height: 1.1;
        letter-spacing: -0.025em;
    }}
    .ab-subtitle {{
        color: {AB_TEXT_MUTED};
        font-size: 1.08rem;
        font-weight: 300;
        margin-top: 0;
        margin-bottom: 1.6rem;
        max-width: 820px;
        line-height: 1.5;
    }}
    .ab-dot {{ color: {AB_ORANGE}; font-weight: 700; }}

    /* SECCIONES (H2) — línea sobria */
    .ab-section {{ margin: 2rem 0 1rem 0; }}
    .ab-section h2 {{
        font-family: 'Manrope', sans-serif !important;
        color: {AB_TEXT} !important;
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        margin: 0 0 8px 0 !important;
        padding-bottom: 10px !important;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        letter-spacing: -0.015em;
    }}
    .ab-section-num {{
        color: {AB_ORANGE};
        font-weight: 700;
        margin-right: 10px;
    }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{
        background-color: {AB_BG_DEEP} !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }}
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] li {{
        color: {AB_TEXT_SOFT} !important;
    }}
    .ab-tagline {{
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.8rem;
        font-weight: 300;
        text-align: center;
        color: {AB_TEXT_MUTED} !important;
        margin: 4px 0 14px 0;
        line-height: 1.35;
        letter-spacing: 0.2px;
    }}
    .ab-sidebar-label {{
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 2.2px;
        font-weight: 600;
        color: {AB_BLUE_LIGHT} !important;
        margin: 0 0 6px 0;
    }}
    .ab-sidebar-value {{
        font-family: 'Lato', sans-serif !important;
        font-weight: 600;
        font-size: 0.95rem;
        color: {AB_TEXT} !important;
        margin: 0 0 4px 0;
        line-height: 1.3;
    }}
    .ab-sidebar-muted {{
        font-size: 0.8rem;
        color: {AB_TEXT_MUTED} !important;
        margin: 0;
        line-height: 1.45;
    }}
    .ab-toc {{
        font-family: 'Lato', sans-serif !important;
        font-size: 0.88rem;
        color: {AB_TEXT_SOFT} !important;
        padding-left: 20px;
        margin: 0;
    }}
    .ab-toc li {{ margin-bottom: 4px; }}
    .ab-hr {{
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1.2rem 0;
    }}

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 0.92rem;
        padding: 12px 18px;
        background-color: transparent;
        color: {AB_TEXT_MUTED} !important;
        font-weight: 500;
        border-bottom: 2px solid transparent;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color: {AB_TEXT} !important; }}
    .stTabs [aria-selected="true"] {{
        color: {AB_TEXT} !important;
        border-bottom: 2px solid {AB_ORANGE} !important;
        font-weight: 600;
    }}

    /* CARDS */
    .insight-box {{
        background: {AB_BG_ELEV};
        border: 1px solid rgba(255,255,255,0.06);
        border-left: 3px solid {AB_BLUE_BRIGHT};
        padding: 1.2rem 1.4rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-size: 0.96rem;
        line-height: 1.6;
        color: {AB_TEXT_SOFT};
    }}
    .insight-box b {{ color: {AB_TEXT}; }}
    .warn-box {{
        background: rgba(238, 127, 75, 0.08);
        border: 1px solid rgba(238, 127, 75, 0.25);
        border-left: 3px solid {AB_ORANGE};
        padding: 1.2rem 1.4rem;
        border-radius: 6px;
        margin: 1rem 0;
        color: {AB_TEXT_SOFT};
    }}
    .warn-box b {{ color: {AB_ORANGE_BRIGHT}; }}

    /* MÉTRICAS */
    [data-testid="stMetric"] {{
        background: {AB_BG_ELEV};
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 8px;
        padding: 14px 18px;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Manrope', sans-serif !important;
        color: {AB_TEXT} !important;
        font-weight: 700 !important;
        font-size: 1.7rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {AB_TEXT_MUTED} !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.3px;
    }}

    /* TABLAS */
    [data-testid="stDataFrame"] {{
        background: {AB_BG_ELEV};
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.06);
    }}
    [data-testid="stDataFrame"] * {{
        font-family: 'Lato', sans-serif !important;
        color: {AB_TEXT_SOFT} !important;
    }}

    /* INPUTS */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {{
        background-color: {AB_BG_ELEV} !important;
        border-color: rgba(255,255,255,0.1) !important;
        color: {AB_TEXT} !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {AB_ORANGE} !important;
        box-shadow: 0 0 0 1px {AB_ORANGE}40;
    }}
    .stTextInput label, .stSelectbox label {{
        color: {AB_TEXT_MUTED} !important;
        font-size: 0.85rem !important;
    }}

    /* FOOTER */
    .ab-footer {{
        text-align: center;
        color: {AB_TEXT_MUTED};
        font-size: 0.82rem;
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-weight: 300;
    }}

    /* Plotly transparent */
    .js-plotly-plot .plotly .main-svg {{ background: transparent !important; }}
    </style>
    """, unsafe_allow_html=True)


# ====================================================================
# HELPER — encabezado de sección
# ====================================================================
def ab_section(title: str, number: str = None):
    num_html = (f'<span class="ab-section-num">{number}</span>'
                if number else '')
    st.markdown(
        f'<div class="ab-section"><h2>{num_html}{title}</h2></div>',
        unsafe_allow_html=True,
    )
