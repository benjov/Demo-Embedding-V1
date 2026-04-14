"""
=====================================================================
 analítica boutique · demo
 análisis semántico de riesgo fiscal y regulatorio
=====================================================================

Aplicación Streamlit para presentación a potenciales clientes.
Envuelve el pipeline del notebook de embeddings + PCA + convex hull
en una narrativa de 5 casos de aplicación.

Identidad visual: manual corporativo de Analítica Boutique
 · azul corporativo   #3C4981  (Pantone 280 U)
 · naranja acento     #EE7F4B  (Pantone 158 U, "el punto")
 · títulos            Century Gothic
 · cuerpo             Calibri

Uso:
    pip install -r requirements.txt
    streamlit run app.py
---------------------------------------------------------------------
"""

import streamlit as st

from data_loader import load_data
from views import (
    view_overview,
    view_repse,
    view_objeto_social,
    view_kyc,
    view_auditoria,
    view_clasificacion,
)
from branding import LOGO_SVG, inject_css


# --------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------
st.set_page_config(
    page_title="analítica boutique · demo",
    page_icon="●",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()


# --------------------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------------------
with st.sidebar:
    # Logo SVG de la marca (reproducción del manual)
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown('<p class="ab-tagline">basando decisiones<br/>en el análisis de datos</p>',
                unsafe_allow_html=True)

    st.markdown('<hr class="ab-hr"/>', unsafe_allow_html=True)

    st.markdown('<p class="ab-sidebar-label">caso de estudio</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="ab-sidebar-value">MetalTécnica del Centro, S.A. de C.V.</p>'
                '<p class="ab-sidebar-muted">Industria metal-mecánica &middot; '
                'Acta constitutiva &middot; CSF &middot; 94,312 CFDIs</p>',
                unsafe_allow_html=True)

    st.markdown('<hr class="ab-hr"/>', unsafe_allow_html=True)

    st.markdown('<p class="ab-sidebar-label">recorrido</p>', unsafe_allow_html=True)
    st.markdown(
        '<ol class="ab-toc">'
        '<li>visión general</li>'
        '<li>riesgo repse</li>'
        '<li>objeto social vs. cfdi</li>'
        '<li>kyc de proveedores</li>'
        '<li>auditoría asistida</li>'
        '<li>clasificación sat</li>'
        '</ol>', unsafe_allow_html=True)

    st.markdown('<hr class="ab-hr"/>', unsafe_allow_html=True)

    st.markdown(
        '<p class="ab-sidebar-muted">'
        'pipeline técnico:<br/>'
        'LandingAI ADE · GPT-4.1 ·<br/>OpenAI Embeddings · PCA 3D · Convex Hull'
        '</p>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------
# DATOS
# --------------------------------------------------------------------
data = load_data()


# --------------------------------------------------------------------
# CABECERA
# --------------------------------------------------------------------
st.markdown(
    '<h1 class="ab-h1">'
    'an<span class="ab-dot-letter">á<span class="ab-dot">●</span></span>lisis semántico '
    'de riesgo fiscal y regulatorio'
    '</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="ab-subtitle">'
    'cómo convertir actas constitutivas, constancias fiscales y facturas '
    'electrónicas en un mapa de riesgo interpretable.'
    '</p>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------
# TABS
# --------------------------------------------------------------------
tabs = st.tabs([
    "visión general",
    "① riesgo repse",
    "② objeto social vs. cfdi",
    "③ kyc de proveedores",
    "④ auditoría asistida",
    "⑤ clasificación sat",
])

with tabs[0]:
    view_overview(data)
with tabs[1]:
    view_repse(data)
with tabs[2]:
    view_objeto_social(data)
with tabs[3]:
    view_kyc(data)
with tabs[4]:
    view_auditoria(data)
with tabs[5]:
    view_clasificacion(data)


# --------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------
st.markdown(
    '<div class="ab-footer">'
    '<span class="ab-dot">●</span>&nbsp;'
    'demo interno &middot; los datos mostrados son ficticios y se presentan '
    'con fines ilustrativos. la empresa "MetalTécnica del Centro" no existe; '
    'cualquier similitud con una organización real es coincidencia.'
    '</div>',
    unsafe_allow_html=True,
)
