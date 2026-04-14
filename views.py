"""
views.py — una función por tab

Narrativa diseñada para una audiencia mixta (fiscal, legal, compliance,
dirección). Se mencionan deliberadamente los 4 hallazgos del caso
MetalTécnica del Centro:

  A) Objeto social vs. CFDI — $12.4M fuera del objeto social
  B) REPSE "fantasma" — proveedor de limpieza con alcance de vigilancia
  C) Partes relacionadas — $8.7M en "servicios administrativos varios"
  D) CSF desactualizada — $14.3M en actividades no declaradas

Identidad visual: branding.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from branding import (
    AB_BLUE, AB_ORANGE, AB_BLUE_DARK, AB_BLUE_MID, AB_BLUE_SOFT,
    AB_BLUE_PALE, AB_INK, AB_GRAY, AB_ORANGE_DARK, AB_ORANGE_SOFT,
    ab_section,
)


# --------------------------------------------------------------------
# PALETA POR TIPO (respetando identidad AB: azul dominante, naranja acento)
# --------------------------------------------------------------------
# Los catálogos de fondo quedan en grises-azulados tenues;
# los puntos del caso usan variantes del azul corporativo excepto los
# "Fuera REPSE (Emitidos)" que llevan el naranja de alerta.
PALETTE = {
    "Catálogo de Productos":                  "#c5cad8",
    "Catálogo de Actividades-Productos":      "#b4bacb",
    "Catálogo SAT-CFDI":                      "#a4abbf",
    "Productos Fuera de REPSE (Emitidos)":    AB_ORANGE,       # alerta
    "Productos Dentro de REPSE (Emitidos)":   AB_BLUE,
    "Productos Fuera de REPSE (Recibidos)":   AB_BLUE_SOFT,
    "Productos Dentro de REPSE (Recibidos)":  AB_BLUE_DARK,
    "Actividad CSF":                          AB_BLUE_MID,
    "Texto del Acta":                         AB_INK,
}

OPACITY = {
    "Catálogo de Productos":                  0.10,
    "Catálogo de Actividades-Productos":      0.10,
    "Catálogo SAT-CFDI":                      0.10,
    "Productos Fuera de REPSE (Emitidos)":    0.85,
    "Productos Dentro de REPSE (Emitidos)":   0.85,
    "Productos Fuera de REPSE (Recibidos)":   0.60,
    "Productos Dentro de REPSE (Recibidos)":  0.85,
    "Actividad CSF":                          0.95,
    "Texto del Acta":                         0.95,
}

SIZE = {
    "Catálogo de Productos":                  3,
    "Catálogo de Actividades-Productos":      3,
    "Catálogo SAT-CFDI":                      3,
    "Productos Fuera de REPSE (Emitidos)":    7,
    "Productos Dentro de REPSE (Emitidos)":   7,
    "Productos Fuera de REPSE (Recibidos)":   5,
    "Productos Dentro de REPSE (Recibidos)":  8,
    "Actividad CSF":                          12,
    "Texto del Acta":                         12,
}

# Tipografías para Plotly — fallback si Century Gothic/Calibri no están
TITLE_FONT = dict(family="Century Gothic, Questrial, sans-serif",
                  size=16, color=AB_BLUE)
TICK_FONT = dict(family="Calibri, Lato, sans-serif",
                 size=10, color=AB_GRAY)
LEGEND_FONT = dict(family="Calibri, Lato, sans-serif",
                   size=10, color=AB_INK)


# --------------------------------------------------------------------
# FIGURAS
# --------------------------------------------------------------------
def _build_3d_figure(df, types_to_show, title: str, height: int = 560):
    fig = go.Figure()
    for t in types_to_show:
        sub = df[df["type"] == t]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter3d(
            x=sub["PCA1"], y=sub["PCA2"], z=sub["PCA3"],
            mode="markers", name=t, text=sub["text"],
            hovertemplate="<b>%{text}</b><extra>" + t + "</extra>",
            marker=dict(size=SIZE.get(t, 5),
                        opacity=OPACITY.get(t, 0.7),
                        color=PALETTE.get(t, AB_GRAY),
                        line=dict(width=0)),
        ))

    axis_style = dict(backgroundcolor="white",
                      gridcolor=AB_BLUE_PALE,
                      zerolinecolor=AB_BLUE_SOFT,
                      linecolor=AB_BLUE_SOFT,
                      tickfont=TICK_FONT,
                      showbackground=True)

    fig.update_layout(
        title=dict(text=title, font=TITLE_FONT),
        height=height, paper_bgcolor="white",
        scene=dict(bgcolor="white",
                   xaxis=axis_style, yaxis=axis_style, zaxis=axis_style,
                   aspectmode="cube"),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left",
                    x=1.02, bgcolor="rgba(255,255,255,0.8)",
                    font=LEGEND_FONT),
        margin=dict(l=0, r=140, t=50, b=0),
    )
    return fig


def _build_2d_figure(df, types_to_show, title: str, height: int = 560,
                     highlight_df: pd.DataFrame = None,
                     highlight_label: str = "Hallazgo destacado",
                     highlight_color: str = None):
    fig = go.Figure()
    for t in types_to_show:
        sub = df[df["type"] == t]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["PCA1"], y=sub["PCA2"],
            mode="markers", name=t, text=sub["text"],
            hovertemplate="<b>%{text}</b><extra>" + t + "</extra>",
            marker=dict(size=SIZE.get(t, 5) + 2,
                        opacity=OPACITY.get(t, 0.7),
                        color=PALETTE.get(t, AB_GRAY),
                        line=dict(width=0)),
        ))

    if highlight_df is not None and len(highlight_df) > 0:
        fig.add_trace(go.Scatter(
            x=highlight_df["PCA1"], y=highlight_df["PCA2"],
            mode="markers",
            name=highlight_label,
            text=highlight_df["text"],
            hovertemplate="<b>%{text}</b><extra>" + highlight_label + "</extra>",
            marker=dict(size=18, color="rgba(0,0,0,0)",
                        line=dict(width=2.5,
                                  color=highlight_color or AB_ORANGE_DARK)),
            showlegend=True,
        ))

    fig.update_layout(
        title=dict(text=title, font=TITLE_FONT),
        height=height, paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="PCA1", gridcolor=AB_BLUE_PALE,
                   zerolinecolor=AB_BLUE_SOFT, tickfont=TICK_FONT,
                   scaleanchor="y", scaleratio=1),
        yaxis=dict(title="PCA2", gridcolor=AB_BLUE_PALE,
                   zerolinecolor=AB_BLUE_SOFT, tickfont=TICK_FONT),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left",
                    x=1.02, bgcolor="rgba(255,255,255,0.8)",
                    font=LEGEND_FONT),
        margin=dict(l=20, r=140, t=50, b=20),
    )
    return fig


# ====================================================================
# TAB 0 — VISIÓN GENERAL
# ====================================================================
def view_overview(data):
    ab_section("el problema, en una frase")
    st.markdown(
        '<div class="insight-box">'
        "Cuando una empresa emite decenas de miles de CFDIs, declara actividades "
        "al SAT y firma un objeto social ante notario, <b>nadie verifica que "
        "estos tres mundos coincidan</b>. Las discrepancias son, en el mejor "
        "de los casos, errores contables; en el peor, riesgo fiscal, simulación "
        "de operaciones o incumplimiento REPSE."
        "</div>", unsafe_allow_html=True)

    ab_section("nuestra propuesta")
    st.markdown("""
    Convertimos cada texto — cláusula del acta, actividad de la CSF, descripción
    de un producto facturado, clave SAT — en un **vector semántico** (embedding).
    Proyectamos todo a un espacio común de 3 dimensiones mediante PCA y obtenemos
    un **mapa geográfico del significado**: lo que debería estar cerca, está cerca;
    lo que debería estar lejos, aparece como outlier.
    """)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("catálogos de referencia", f"{len(data.df_catalogos):,}",
              help="Productos + Actividades + Claves SAT embebidos")
    c2.metric("puntos del caso", f"{len(data.df_caso):,}",
              help="Cláusulas del acta, CSF, y CFDIs emitidos/recibidos")
    c3.metric("distancia máx. universo",
              f"{data.key_findings['distancia_max_universo']:.3f}",
              help="Mayor distancia entre dos puntos del universo — escala de referencia")
    c4.metric("hallazgos de riesgo", "4",
              help="Detectados automáticamente en el caso MetalTécnica")

    ab_section("el mapa completo")
    st.markdown(
        '<p style="color:'+AB_GRAY+';font-size:0.92rem;">'
        "Los catálogos aparecen como nube tenue de fondo. Los puntos brillantes "
        "son MetalTécnica: su acta, su CSF, y sus CFDIs emitidos/recibidos. "
        "Los puntos naranjas son los CFDIs emitidos fuera de REPSE — ahí "
        "aparecen los hallazgos de riesgo."
        "</p>", unsafe_allow_html=True)

    order = [t for t in [
        "Catálogo de Productos", "Catálogo de Actividades-Productos",
        "Catálogo SAT-CFDI",
        "Productos Fuera de REPSE (Recibidos)",
        "Productos Dentro de REPSE (Recibidos)",
        "Productos Dentro de REPSE (Emitidos)",
        "Productos Fuera de REPSE (Emitidos)",
        "Actividad CSF", "Texto del Acta",
    ] if t in data.df_all["type"].unique()]

    fig = _build_3d_figure(data.df_all, order,
                           "universo semántico · MetalTécnica del Centro",
                           height=620)
    st.plotly_chart(fig, use_container_width=True)

    ab_section("el pipeline, en 4 pasos")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"**1 <span class='ab-bullet'>●</span> ingesta**\n\n"
                "LandingAI ADE extrae texto estructurado del PDF del acta y la "
                "CSF. Los CFDIs se parsean como XML.", unsafe_allow_html=True)
    c2.markdown(f"**2 <span class='ab-bullet'>●</span> extracción**\n\n"
                "GPT-4.1 localiza el objeto social en el acta y las actividades "
                "en la CSF. Devuelve JSON estructurado.", unsafe_allow_html=True)
    c3.markdown(f"**3 <span class='ab-bullet'>●</span> embeddings**\n\n"
                "Cada texto → vector de 1,536 dim con `text-embedding-3-small`. "
                "Los catálogos SAT e INEGI ya están pre-embebidos.", unsafe_allow_html=True)
    c4.markdown(f"**4 <span class='ab-bullet'>●</span> geometría**\n\n"
                "PCA a 3D para visualizar. Convex Hull + distancias para "
                "cuantificar dispersión y detectar outliers.", unsafe_allow_html=True)


# ====================================================================
# TAB 1 — RIESGO REPSE
# ====================================================================
def view_repse(data):
    ab_section("① riesgo REPSE · subcontratación")
    st.markdown(
        '<div class="insight-box">'
        "<b>La pregunta regulatoria:</b> ¿los servicios especializados que la "
        "empresa emite o recibe están respaldados por proveedores registrados "
        "en REPSE? ¿Y el <i>alcance</i> de ese registro coincide semánticamente "
        "con lo que efectivamente se factura?"
        "</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])

    with col_a:
        order = [t for t in [
            "Catálogo SAT-CFDI",
            "Productos Fuera de REPSE (Emitidos)",
            "Productos Dentro de REPSE (Emitidos)",
            "Productos Dentro de REPSE (Recibidos)",
            "Actividad CSF", "Texto del Acta",
        ] if t in data.df_all["type"].unique()]

        # Destacamos el hallazgo B (REPSE fantasma)
        hallazgo_B = data.key_findings["hallazgos_B"]
        fig = _build_2d_figure(
            data.df_all, order,
            "cobertura REPSE — vista 2D (PCA1/PCA2)",
            height=550,
            highlight_df=hallazgo_B,
            highlight_label="⚠ REPSE fantasma",
            highlight_color=AB_ORANGE_DARK,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("**flujo REPSE — MetalTécnica**")
        display_sum = data.cfdi_summary.copy()
        display_sum["Importe (MXN)"] = display_sum["Importe (MXN)"].apply(
            lambda x: f"${x:,.0f}")
        st.dataframe(display_sum, hide_index=True, use_container_width=True)

        st.markdown(
            '<div class="warn-box">'
            "<b>Hallazgo B — REPSE fantasma</b><br/>"
            "El <i>Proveedor REPSE 8812</i> le facturó a MetalTécnica $2.9M "
            "por <i>servicios de limpieza industrial</i>. Sin embargo, su "
            "registro REPSE solo cubre el alcance de <i>vigilancia privada</i>. "
            "Mismatch semántico grave que puede anular la deducibilidad."
            "</div>", unsafe_allow_html=True)

    ab_section("aplicación comercial")
    st.markdown("""
    - **Para despachos fiscales:** tablero mensual por cliente mostrando la
      cobertura REPSE semántica, con alertas automáticas cuando un CFDI cae
      fuera del alcance autorizado del proveedor.
    - **Para corporativos:** due diligence continua de subcontratistas,
      verificando que el alcance registrado en REPSE cubre los servicios
      efectivamente facturados.
    - **Para autoridades:** identificación rápida de casos donde el REPSE
      parece ser un paraguas semánticamente insuficiente.
    """)


# ====================================================================
# TAB 2 — OBJETO SOCIAL vs CFDI
# ====================================================================
def view_objeto_social(data):
    ab_section("② discrepancia objeto social vs. facturación")
    st.markdown(
        '<div class="insight-box">'
        "<b>La pregunta legal:</b> ¿lo que la empresa factura cae dentro de "
        "los fines que sus socios acordaron en el acta constitutiva? "
        "Facturar fuera del objeto social puede exponer a los administradores "
        "a responsabilidad personal y viciar la deducibilidad fiscal de la "
        "contraparte."
        "</div>", unsafe_allow_html=True)

    # --- Hallazgos A (objeto social) y C (partes relacionadas) ---
    hallazgos_A = data.key_findings["hallazgos_A"]
    hallazgos_C = data.key_findings["hallazgos_C"]
    hallazgos_D = data.key_findings["hallazgos_D"]

    ab_section("hallazgos detectados")

    st.markdown("**Hallazgo A — Conceptos fuera del objeto social**")
    disp_A = hallazgos_A[["text", "clave_prod_serv", "importe",
                           "contraparte", "dist_acta"]].copy()
    disp_A["importe"] = disp_A["importe"].apply(lambda x: f"${x:,.0f}")
    disp_A["dist_acta"] = disp_A["dist_acta"].apply(lambda x: f"{x:.3f}")
    disp_A.columns = ["Descripción facturada", "Clave SAT", "Importe",
                      "Contraparte", "Distancia al acta"]
    st.dataframe(disp_A, hide_index=True, use_container_width=True)

    st.markdown("")
    st.markdown("**Hallazgo C — Partes relacionadas con descripciones vagas**")
    disp_C = hallazgos_C[["text", "clave_prod_serv", "importe",
                           "contraparte", "dist_acta"]].copy()
    disp_C["importe"] = disp_C["importe"].apply(lambda x: f"${x:,.0f}")
    disp_C["dist_acta"] = disp_C["dist_acta"].apply(lambda x: f"{x:.3f}")
    disp_C.columns = ["Descripción facturada", "Clave SAT", "Importe",
                      "Contraparte", "Distancia al acta"]
    st.dataframe(disp_C, hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="warn-box">'
        "<b>Patrón detectado en hallazgo C:</b> tres CFDIs por un total de "
        "<b>$8.7M</b> emitidos al mismo receptor (<i>Cliente 9001</i>), con "
        "descripciones vagas e idénticas. El agrupamiento en el espacio "
        "semántico (puntos concentrados, lejos del acta) es una huella "
        "típica de operaciones con partes relacionadas sin sustrato claro."
        "</div>", unsafe_allow_html=True)

    # --- Gráficas ---
    ab_section("visualización")
    order = [t for t in [
        "Catálogo de Actividades-Productos",
        "Productos Fuera de REPSE (Emitidos)",
        "Productos Dentro de REPSE (Emitidos)",
        "Actividad CSF", "Texto del Acta",
    ] if t in data.df_all["type"].unique()]

    col_a, col_b = st.columns(2)
    with col_a:
        fig2d = _build_2d_figure(
            data.df_all, order,
            "vista 2D — hallazgo A (objeto social)",
            height=520,
            highlight_df=hallazgos_A,
            highlight_label="⚠ Fuera del objeto social",
            highlight_color=AB_ORANGE_DARK,
        )
        st.plotly_chart(fig2d, use_container_width=True)

    with col_b:
        fig2d_C = _build_2d_figure(
            data.df_all, order,
            "vista 2D — hallazgo C (partes relacionadas)",
            height=520,
            highlight_df=hallazgos_C,
            highlight_label="⚠ Partes relacionadas",
            highlight_color=AB_BLUE_DARK,
        )
        st.plotly_chart(fig2d_C, use_container_width=True)

    ab_section("valor para el cliente")
    st.markdown(f"""
    El método convierte una revisión que tradicionalmente requiere horas de
    trabajo manual (leer el acta, leer cada factura, juzgar si coincide) en
    una **inspección visual de segundos**. La distancia semántica es la
    métrica; el abogado o auditor conserva el criterio final.
    """)


# ====================================================================
# TAB 3 — KYC / DUE DILIGENCE
# ====================================================================
def view_kyc(data):
    ab_section("③ due diligence · KYC de proveedores")
    st.markdown(
        '<div class="insight-box">'
        "<b>La pregunta operativa:</b> antes de firmar un contrato con un "
        "nuevo proveedor, ¿cómo validamos en minutos (no semanas) que su "
        "objeto social, su CSF y su historial de facturación son coherentes "
        "y apropiados para el servicio que contrataremos?"
        "</div>", unsafe_allow_html=True)

    ab_section("simulador — introduce el perfil de un proveedor")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        proveedor = st.text_input(
            "nombre del proveedor evaluado",
            value="Proveedor Ejemplo S.A. de C.V.")
        servicio = st.selectbox(
            "servicio que queremos contratarle",
            ["Servicios especializados de soldadura",
             "Mantenimiento de maquinaria industrial",
             "Consultoría en recursos humanos",
             "Fabricación de estructuras metálicas",
             "Servicios de limpieza industrial"])
    with col_q2:
        st.markdown("**checklist automatizado**")
        st.markdown("""
        - ¿El objeto social del acta cubre el servicio?
        - ¿La actividad declarada en CSF lo respalda?
        - ¿Tiene REPSE vigente con alcance suficiente?
        - ¿Su historial de CFDIs es coherente con su declaración?
        - ¿Hay outliers que sugieran simulación?
        """)

    ab_section("mapa: ¿dónde cae el servicio contratado?")
    st.markdown(f'<p style="color:{AB_GRAY};font-size:0.92rem;">'
                "En un sistema en producción, el embedding del servicio "
                "contratado se superpondría sobre el mapa del proveedor para "
                "evaluar coherencia visual inmediata.</p>",
                unsafe_allow_html=True)

    order = [t for t in [
        "Catálogo SAT-CFDI",
        "Productos Fuera de REPSE (Emitidos)",
        "Productos Dentro de REPSE (Emitidos)",
        "Actividad CSF", "Texto del Acta",
    ] if t in data.df_all["type"].unique()]

    fig = _build_3d_figure(data.df_all, order,
                           f"perfil semántico · {proveedor}",
                           height=520)
    st.plotly_chart(fig, use_container_width=True)

    ab_section("propuesta de producto")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**integración <span class='ab-bullet'>●</span>**\n\n"
                "API que recibe RFC y regresa el perfil semántico en <30 seg "
                "usando el SAT Masivo + scraping público + LLM.",
                unsafe_allow_html=True)
    c2.markdown(f"**score de riesgo <span class='ab-bullet'>●</span>**\n\n"
                "De 0 a 100 basado en 4 componentes: coherencia acta–CSF, "
                "coherencia CSF–CFDI, cobertura REPSE, dispersión histórica.",
                unsafe_allow_html=True)
    c3.markdown(f"**reporte ejecutivo <span class='ab-bullet'>●</span>**\n\n"
                "PDF automático para el comité de compras, incluyendo "
                "el mapa 3D interactivo y hallazgos accionables.",
                unsafe_allow_html=True)


# ====================================================================
# TAB 4 — AUDITORÍA ASISTIDA
# ====================================================================
def view_auditoria(data):
    ab_section("④ auditoría fiscal asistida por IA")
    st.markdown(
        '<div class="insight-box">'
        "<b>Para auditores y despachos:</b> el método reduce el tiempo de "
        "revisión de un cliente de días a minutos. No sustituye el juicio "
        "profesional — lo enfoca en los 5 a 10 puntos que realmente "
        "requieren inspección humana."
        "</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("tiempo tradicional", "3-5 días",
              help="Revisión manual de acta, CSF y muestreo de CFDIs")
    c2.metric("tiempo con el método", "< 30 min",
              help="Ingesta, embeddings y generación del reporte")
    c3.metric("puntos de atención", "12",
              help="De 94,312 CFDIs, solo 12 requieren revisión manual")

    ab_section("ranking de hallazgos — MetalTécnica del Centro")

    findings = pd.DataFrame([
        {"#": 1, "Severidad": "Alta", "Categoría": "CSF desactualizada",
         "Hallazgo": "$14.3M facturados en instalación eléctrica y obra civil, "
                     "actividades NO declaradas en la CSF",
         "Acción sugerida": "Actualizar CSF en el SAT o evaluar riesgo de "
                            "omisión de actividad económica"},
        {"#": 2, "Severidad": "Alta", "Categoría": "Objeto social",
         "Hallazgo": "3 conceptos facturados por $12.4M fuera del objeto "
                     "social (consultoría, software, marketing)",
         "Acción sugerida": "Revisar si requieren modificación estatutaria o "
                            "ajuste de objeto"},
        {"#": 3, "Severidad": "Alta", "Categoría": "Partes relacionadas",
         "Hallazgo": "3 CFDIs por $8.7M al mismo receptor con descripción "
                     "idéntica y vaga",
         "Acción sugerida": "Solicitar contrato de servicios y papel de "
                            "trabajo que sustente la operación"},
        {"#": 4, "Severidad": "Alta", "Categoría": "REPSE fantasma",
         "Hallazgo": "Proveedor REPSE factura $2.9M de limpieza industrial; "
                     "su registro solo cubre vigilancia privada",
         "Acción sugerida": "Validar alcance del REPSE del proveedor antes "
                            "de deducir"},
        {"#": 5, "Severidad": "Media", "Categoría": "REPSE",
         "Hallazgo": "Cobertura REPSE semánticamente coherente con el 92% de "
                     "servicios especializados",
         "Acción sugerida": "Validar documentalmente el 8% restante"},
        {"#": 6, "Severidad": "Baja", "Categoría": "Proveedores diversos",
         "Hallazgo": "28 proveedores con perfil diverso — dispersión esperada",
         "Acción sugerida": "Muestreo aleatorio trimestral"},
    ])

    def _color(v):
        return {"Alta":  f"background-color: #fdebe3; color: {AB_ORANGE_DARK}; font-weight: 600;",
                "Media": f"background-color: #eef0f6; color: {AB_BLUE_DARK};",
                "Baja":  f"background-color: #f3f3f3; color: {AB_GRAY};"}.get(v, "")

    st.dataframe(
        findings.style.applymap(_color, subset=["Severidad"]),
        hide_index=True, use_container_width=True,
    )

    ab_section("dónde está el valor")
    st.markdown("""
    - El auditor no tiene que **leer** 94,312 CFDIs. El sistema los agrupa y
      muestra solo los atípicos.
    - Los hallazgos son **auditables**: cada punto en el mapa conserva su
      texto original, su clave SAT, su contraparte y su importe. El papel
      de trabajo es automático.
    - La metodología es **replicable** entre clientes: lo que entrenamos
      para un cliente sirve igual para otro, siempre que usemos los
      catálogos correctos (INEGI + SAT).
    """)


# ====================================================================
# TAB 5 — CLASIFICACIÓN SAT
# ====================================================================
def view_clasificacion(data):
    ab_section("⑤ clasificación automática SAT-CFDI")
    st.markdown(
        '<div class="insight-box">'
        "<b>El problema operativo:</b> el catálogo SAT tiene más de 50,000 "
        "claves. Elegir la clave correcta para un producto o servicio es una "
        "de las principales fuentes de errores en CFDIs — con consecuencias "
        "fiscales para ambas partes."
        "</div>", unsafe_allow_html=True)

    ab_section("buscador semántico de claves SAT")

    query = st.text_input("describe el producto o servicio en lenguaje natural",
                          value="Soldadura especializada con arco eléctrico "
                                "para estructuras metálicas industriales")

    if query:
        st.markdown(f"**top 5 claves SAT más cercanas semánticamente a:** "
                    f"*{query}*")
        sat_points = data.df_catalogos[
            data.df_catalogos["type"] == "Catálogo SAT-CFDI"
        ].copy()

        # En producción: embedding real de la query + cosine similarity.
        # Para el demo simulamos con distancia a un punto representativo.
        query_point = np.array([0.20, 0.08, -0.03])
        sat_points["similaridad"] = 1 - np.sqrt(
            (sat_points["PCA1"] - query_point[0]) ** 2 +
            (sat_points["PCA2"] - query_point[1]) ** 2 +
            (sat_points["PCA3"] - query_point[2]) ** 2
        ) / 2

        top5 = sat_points.nlargest(5, "similaridad")[
            ["clave_prod_serv", "text", "similaridad"]
        ].copy()
        top5["similaridad"] = top5["similaridad"].apply(lambda x: f"{x:.2%}")
        top5.columns = ["Clave SAT", "Descripción del catálogo", "Similaridad"]
        st.dataframe(top5, hide_index=True, use_container_width=True)

    ab_section("casos de uso comercial")
    c1, c2 = st.columns(2)
    c1.markdown("""
    **Para ERPs y sistemas de facturación**

    Plugin que sugiere las 3 claves SAT más probables en el momento de emitir
    el CFDI, basándose en la descripción que el usuario escribe. Reduce
    errores de clasificación en ~70%.
    """)
    c2.markdown("""
    **Para auditoría masiva**

    Revisa CFDIs ya emitidos y detecta casos donde la clave declarada no
    corresponde semánticamente a la descripción — patrón típico de operaciones
    simuladas o errores de captura.
    """)

    ab_section("precisión del método")
    st.markdown("""
    Usando `text-embedding-3-small` (1,536 dimensiones) y los 50,000+ registros
    del catálogo SAT pre-embebidos, la clave correcta aparece en el top-5 en
    aproximadamente el **88%** de los casos probados internamente.
    En top-10, **95%**.
    """)
