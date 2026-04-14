"""
=====================================================================
 analítica boutique · demo
 análisis semántico de riesgo fiscal y regulatorio
=====================================================================
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
    st.markdown('<p class="ab-tagline">Precisión analítica,<br/>visión estratégica</p>',
                unsafe_allow_html=True)

    st.markdown('<hr class="ab-hr"/>', unsafe_allow_html=True)

    st.markdown('<p class="ab-sidebar-label">Caso de estudio</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="ab-sidebar-value">MetalTécnica del Centro, S.A. de C.V.</p>'
                '<p class="ab-sidebar-muted">Industria metal-mecánica<br/>'
                'Acta constitutiva · CSF · +94,000 CFDIs</p>',
                unsafe_allow_html=True)

    st.markdown('<hr class="ab-hr"/>', unsafe_allow_html=True)

    st.markdown('<p class="ab-sidebar-label">recorrido</p>', unsafe_allow_html=True)
    st.markdown(
        '<ol class="ab-toc">'
        '<li>Visión general</li>'
        '<li>Riesgo REPSE</li>'
        '<li>Objeto social vs. CFDI</li>'
        '<li>KYC de proveedores</li>'
        '<li>Auditoría asistida</li>'
        '<li>Clasificación SAT</li>'
        '</ol>', unsafe_allow_html=True)

    st.markdown('<hr class="ab-hr"/>', unsafe_allow_html=True)

    st.markdown(
        '<p class="ab-sidebar-muted">'
        'pipeline técnico:<br/>'
        'OCR · GPT-4.1 · OpenAI Embeddings · <br/>PCA 3D · Convex Hull'
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
    'Precisión analítica aplicada al riesgo fiscal'
    '</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="ab-subtitle">'
    'Convertimos actas constitutivas, Constancias se Situación Fiscal (CSF) y facturas '
    'electrónicas en un mapa de riesgo interpretable — <b>transformando '
    'información compleja en ventajas competitivas tangibles y medibles</b>.'
    '</p>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------
# TABS
# --------------------------------------------------------------------
tabs = st.tabs([
    "Visión general",
    "Riesgo REPSE",
    "Objeto social vs. CFDI",
    "KYC de proveedores",
    "Auditoría asistida",
    "Clasificación SAT",
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
    'Demo interno · Los datos mostrados son ficticios y se presentan '
    'con fines ilustrativos. La empresa "MetalTécnica del Centro" no existe; '
    'cualquier similitud con una organización real es coincidencia.'
    '</div>',
    unsafe_allow_html=True,
)
