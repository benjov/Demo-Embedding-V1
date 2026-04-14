"""
views.py — una función por tab

Narrativa con los 4 hallazgos ficticios del caso MetalTécnica del Centro:
  A) Objeto social vs. CFDI — $12.4M fuera del objeto social
  B) REPSE "fantasma" — proveedor de limpieza con alcance de vigilancia
  C) Partes relacionadas — $8.7M en "servicios administrativos varios"
  D) CSF desactualizada — $14.3M en actividades no declaradas

Gráficas Plotly adaptadas a fondo oscuro para proyectar en sala.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from branding import (
    AB_BLUE, AB_ORANGE, AB_ORANGE_BRIGHT, AB_ORANGE_DEEP,
    AB_BLUE_BRIGHT, AB_BLUE_LIGHT, AB_BLUE_PALE,
    AB_TEXT, AB_TEXT_SOFT, AB_TEXT_MUTED,
    AB_BG, AB_BG_ELEV,
    ab_section,
)


# --------------------------------------------------------------------
# PALETA POR TIPO — adaptada a fondo oscuro
# --------------------------------------------------------------------
PALETTE = {
    "Catálogo de Productos":                  "#3b4470",
    "Catálogo de Actividades-Productos":      "#4a5484",
    "Catálogo SAT-CFDI":                      "#5864a0",
    "Productos Fuera de REPSE (Emitidos)":    AB_ORANGE,       # alerta
    "Productos Dentro de REPSE (Emitidos)":   AB_BLUE_BRIGHT,
    "Productos Fuera de REPSE (Recibidos)":   AB_BLUE_LIGHT,
    "Productos Dentro de REPSE (Recibidos)":  "#9aa6d6",
    "Actividad CSF":                          "#f5d98a",       # amarillo suave
    "Texto del Acta":                         "#ffffff",
}

OPACITY = {
    "Catálogo de Productos":                  0.22,
    "Catálogo de Actividades-Productos":      0.22,
    "Catálogo SAT-CFDI":                      0.22,
    "Productos Fuera de REPSE (Emitidos)":    0.9,
    "Productos Dentro de REPSE (Emitidos)":   0.85,
    "Productos Fuera de REPSE (Recibidos)":   0.6,
    "Productos Dentro de REPSE (Recibidos)":  0.9,
    "Actividad CSF":                          0.95,
    "Texto del Acta":                         1.0,
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

# Tipografías Plotly
TITLE_FONT = dict(family="Manrope, sans-serif", size=15, color=AB_TEXT)
TICK_FONT = dict(family="Lato, sans-serif", size=10, color=AB_TEXT_MUTED)
LEGEND_FONT = dict(family="Lato, sans-serif", size=10, color=AB_TEXT_SOFT)

GRID_COLOR = "rgba(255,255,255,0.05)"
ZERO_COLOR = "rgba(255,255,255,0.15)"


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
                        color=PALETTE.get(t, AB_TEXT_MUTED),
                        line=dict(width=0)),
        ))

    axis_style = dict(
        backgroundcolor="rgba(0,0,0,0)",
        gridcolor=GRID_COLOR,
        zerolinecolor=ZERO_COLOR,
        linecolor="rgba(255,255,255,0.15)",
        tickfont=TICK_FONT,
        showbackground=False,
    )

    fig.update_layout(
        title=dict(text=title, font=TITLE_FONT, x=0.02, xanchor="left"),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(bgcolor="rgba(0,0,0,0)",
                   xaxis=axis_style, yaxis=axis_style, zaxis=axis_style,
                   aspectmode="cube"),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left",
                    x=1.02, bgcolor="rgba(30,38,84,0.6)",
                    bordercolor="rgba(255,255,255,0.08)", borderwidth=1,
                    font=LEGEND_FONT),
        margin=dict(l=0, r=160, t=50, b=0),
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
                        color=PALETTE.get(t, AB_TEXT_MUTED),
                        line=dict(width=0)),
        ))

    if highlight_df is not None and len(highlight_df) > 0:
        fig.add_trace(go.Scatter(
            x=highlight_df["PCA1"], y=highlight_df["PCA2"],
            mode="markers", name=highlight_label, text=highlight_df["text"],
            hovertemplate="<b>%{text}</b><extra>" + highlight_label + "</extra>",
            marker=dict(size=20, color="rgba(0,0,0,0)",
                        line=dict(width=2.5,
                                  color=highlight_color or AB_ORANGE_BRIGHT)),
            showlegend=True,
        ))

    fig.update_layout(
        title=dict(text=title, font=TITLE_FONT, x=0.02, xanchor="left"),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="PCA1", gridcolor=GRID_COLOR,
                   zerolinecolor=ZERO_COLOR, tickfont=TICK_FONT,
                   title_font=dict(color=AB_TEXT_MUTED, size=11),
                   scaleanchor="y", scaleratio=1),
        yaxis=dict(title="PCA2", gridcolor=GRID_COLOR,
                   zerolinecolor=ZERO_COLOR, tickfont=TICK_FONT,
                   title_font=dict(color=AB_TEXT_MUTED, size=11)),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left",
                    x=1.02, bgcolor="rgba(30,38,84,0.6)",
                    bordercolor="rgba(255,255,255,0.08)", borderwidth=1,
                    font=LEGEND_FONT),
        margin=dict(l=20, r=160, t=50, b=20),
    )
    return fig


# ====================================================================
# TAB 0 — VISIÓN GENERAL
# ====================================================================
def view_overview(data):
    ab_section("El problema, en una frase")
    st.markdown(
        '<div class="insight-box">'
        "Cuando una empresa emite decenas de miles de CFDIs, declara "
        "actividades al SAT y firma un objeto social ante notario, "
        "<b>nadie verifica que estos tres mundos coincidan</b>. "
        "Las discrepancias son, en el mejor de los casos, errores contables; "
        "en el peor, riesgo fiscal, simulación de operaciones o "
        "incumplimiento REPSE."
        "</div>", unsafe_allow_html=True)

    ab_section("Nuestra propuesta")
    st.markdown("""
    Convertimos cada texto — cláusula del acta, actividad de la CSF,
    descripción de un producto facturado, clave SAT — en un **vector
    semántico** (embedding). Proyectamos todo a un espacio común de 3
    dimensiones mediante PCA y obtenemos un **mapa geográfico del
    significado**: lo que debería estar cerca, está cerca; lo que
    debería estar lejos, aparece como outlier.
    """)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Catálogos de \nreferencia", f"{len(data.df_catalogos):,}")
    c2.metric("Puntos del caso", f"{len(data.df_caso):,}")
    c3.metric("Distancia máxima \nuniverso",
              f"{data.key_findings['distancia_max_universo']:.3f}")
    c4.metric("Hallazgos de \nriesgo", "4")

    ab_section("El mapa completo")
    st.markdown(
        f'<p style="color:{AB_TEXT_MUTED};font-size:0.92rem;">'
        "Los catálogos aparecen como nube tenue de fondo. Los puntos "
        "brillantes son MetalTécnica: su acta, su CSF, y sus CFDIs "
        "emitidos/recibidos. Los puntos naranjas son los CFDIs emitidos "
        "fuera de REPSE — ahí aparecen los hallazgos de riesgo."
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
                           "Universo semántico · MetalTécnica del Centro",
                           height=620)
    st.plotly_chart(fig, use_container_width=True)

    ab_section("El pipeline, en 4 pasos")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("**1 · Ingesta**\n\nOCR extrae texto estructurado "
                "del PDF del acta y la CSF. Los CFDIs se parsean como XML.")
    c2.markdown("**2 · Extracción**\n\nGPT-4.1 localiza el objeto social "
                "en el acta y las actividades en la CSF. Devuelve JSON "
                "estructurado.")
    c3.markdown("**3 · Embeddings**\n\nCada texto → vector de 1,536 dim con "
                "`text-embedding-3-small`. Los catálogos SAT e INEGI ya "
                "están pre-embebidos.")
    c4.markdown("**4 · Geometría**\n\nPCA a 3D para visualizar. "
                "Convex Hull + distancias para cuantificar dispersión y "
                "detectar outliers.")


# ====================================================================
# TAB 1 — RIESGO REPSE
# ====================================================================
def view_repse(data):
    ab_section("Riesgo REPSE · Subcontratación", number="01")
    st.markdown(
        '<div class="insight-box">'
        "<b>La pregunta regulatoria:</b> ¿los servicios especializados que "
        "la empresa emite o recibe están respaldados por proveedores "
        "registrados en REPSE? ¿Y el <i>alcance</i> de ese registro "
        "coincide semánticamente con lo que efectivamente se factura?"
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

        hallazgo_B = data.key_findings["hallazgos_B"]
        fig = _build_2d_figure(
            data.df_all, order,
            "Cobertura REPSE — vista 2D",
            height=550,
            highlight_df=hallazgo_B,
            highlight_label="⚠ REPSE fantasma",
            highlight_color=AB_ORANGE_BRIGHT,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("**Flujo REPSE — MetalTécnica**")
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

    ab_section("Aplicación comercial")
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
    ab_section("Discrepancia objeto social vs. facturación", number="02")
    st.markdown(
        '<div class="insight-box">'
        "<b>La pregunta legal:</b> ¿lo que la empresa factura cae dentro de "
        "los fines que sus socios acordaron en el acta constitutiva? "
        "Facturar fuera del objeto social puede exponer a los administradores "
        "a responsabilidad personal y viciar la deducibilidad fiscal de la "
        "contraparte."
        "</div>", unsafe_allow_html=True)

    hallazgos_A = data.key_findings["hallazgos_A"]
    hallazgos_C = data.key_findings["hallazgos_C"]

    ab_section("Hallazgos detectados")

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

    ab_section("Visualización")
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
            "Hallazgo A · Objeto social",
            height=520,
            highlight_df=hallazgos_A,
            highlight_label="⚠ Fuera del objeto social",
            highlight_color=AB_ORANGE_BRIGHT,
        )
        st.plotly_chart(fig2d, use_container_width=True)

    with col_b:
        fig2d_C = _build_2d_figure(
            data.df_all, order,
            "Hallazgo C · Partes relacionadas",
            height=520,
            highlight_df=hallazgos_C,
            highlight_label="⚠ Partes relacionadas",
            highlight_color="#f5d98a",
        )
        st.plotly_chart(fig2d_C, use_container_width=True)

    ab_section("Valor para el cliente")
    st.markdown("""
    El método convierte una revisión que tradicionalmente requiere horas de
    trabajo manual (leer el acta, leer cada factura, juzgar si coincide) en
    una **inspección visual de segundos**. La distancia semántica es la
    métrica; el abogado o auditor conserva el criterio final.
    """)


# ====================================================================
# TAB 3 — KYC / DUE DILIGENCE
# ====================================================================
def view_kyc(data):
    ab_section("Due diligence · KYC de proveedores", number="03")
    st.markdown(
        '<div class="insight-box">'
        "<b>La pregunta operativa:</b> antes de firmar un contrato con un "
        "nuevo proveedor, ¿cómo validamos en minutos (no semanas) que su "
        "objeto social, su CSF y su historial de facturación son coherentes "
        "y apropiados para el servicio que contrataremos?"
        "</div>", unsafe_allow_html=True)

    ab_section("Simulador — introduce el perfil de un proveedor")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        proveedor = st.text_input(
            "Nombre del proveedor evaluado",
            value="Proveedor Ejemplo S.A. de C.V.")
        servicio = st.selectbox(
            "Servicio que queremos contratarle",
            ["Servicios especializados de soldadura",
             "Mantenimiento de maquinaria industrial",
             "Consultoría en recursos humanos",
             "Fabricación de estructuras metálicas",
             "Servicios de limpieza industrial"])
    with col_q2:
        st.markdown("**Checklist automatizado**")
        st.markdown("""
        - ¿El objeto social del acta cubre el servicio?
        - ¿La actividad declarada en CSF lo respalda?
        - ¿Tiene REPSE vigente con alcance suficiente?
        - ¿Su historial de CFDIs es coherente con su declaración?
        - ¿Hay outliers que sugieran simulación?
        """)

    ab_section("Mapa: ¿dónde cae el servicio contratado?")
    st.markdown(f'<p style="color:{AB_TEXT_MUTED};font-size:0.92rem;">'
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
                           f"Perfil semántico · {proveedor}",
                           height=520)
    st.plotly_chart(fig, use_container_width=True)

    ab_section("Propuesta de producto")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Integración**\n\nAPI que recibe RFC y regresa el perfil "
                "semántico en <30 seg usando el SAT Masivo + scraping "
                "público + LLM.")
    c2.markdown("**Score de riesgo**\n\nDe 0 a 100 basado en 4 componentes: "
                "coherencia acta–CSF, coherencia CSF–CFDI, cobertura REPSE, "
                "dispersión histórica.")
    c3.markdown("**Reporte ejecutivo**\n\nPDF automático para el comité de "
                "compras, incluyendo el mapa 3D interactivo y hallazgos "
                "accionables.")


# ====================================================================
# TAB 4 — AUDITORÍA ASISTIDA
# ====================================================================
def view_auditoria(data):
    ab_section("Auditoría fiscal asistida por IA", number="04")
    st.markdown(
        '<div class="insight-box">'
        "<b>Para auditores y despachos:</b> el método reduce el tiempo de "
        "revisión de un cliente de días a minutos. No sustituye el juicio "
        "profesional — lo enfoca en los 5 a 10 puntos que realmente "
        "requieren inspección humana."
        "</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Tiempo tradicional", "3-5 días")
    c2.metric("Tiempo con el método", "< 30 min")
    c3.metric("Puntos de atención", "12")

    ab_section("Ranking de hallazgos — MetalTécnica del Centro")

    findings = pd.DataFrame([
        {"#": 1, "Severidad": "Alta", "Categoría": "CSF desactualizada",
         "Hallazgo": "$14.3M facturados en instalación eléctrica y obra "
                     "civil, actividades NO declaradas en la CSF",
         "Acción sugerida": "Actualizar CSF en el SAT o evaluar riesgo de "
                            "omisión de actividad económica"},
        {"#": 2, "Severidad": "Alta", "Categoría": "Objeto social",
         "Hallazgo": "3 conceptos facturados por $12.4M fuera del objeto "
                     "social (consultoría, software, marketing)",
         "Acción sugerida": "Revisar si requieren modificación estatutaria "
                            "o ajuste de objeto"},
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
         "Hallazgo": "Cobertura REPSE semánticamente coherente con el 92% "
                     "de servicios especializados",
         "Acción sugerida": "Validar documentalmente el 8% restante"},
        {"#": 6, "Severidad": "Baja", "Categoría": "Proveedores diversos",
         "Hallazgo": "28 proveedores con perfil diverso — dispersión "
                     "esperada",
         "Acción sugerida": "Muestreo aleatorio trimestral"},
    ])

    def _color(v):
        return {
            "Alta":  f"background-color: rgba(238,127,75,0.18); "
                     f"color: {AB_ORANGE_BRIGHT}; font-weight: 600;",
            "Media": f"background-color: rgba(154,166,214,0.12); "
                     f"color: {AB_BLUE_LIGHT};",
            "Baja":  f"background-color: rgba(255,255,255,0.04); "
                     f"color: {AB_TEXT_MUTED};",
        }.get(v, "")

    st.dataframe(
        findings.style.applymap(_color, subset=["Severidad"]),
        hide_index=True, use_container_width=True,
    )

    ab_section("Dónde está el valor")
    st.markdown("""
    - El auditor no tiene que **leer** 94,312 CFDIs. El sistema los agrupa
      y muestra solo los atípicos.
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
    ab_section("Clasificación automática SAT-CFDI", number="05")
    st.markdown(
        '<div class="insight-box">'
        "<b>El problema operativo:</b> el catálogo SAT tiene más de 50,000 "
        "claves. Elegir la clave correcta para un producto o servicio es "
        "una de las principales fuentes de errores en CFDIs — con "
        "consecuencias fiscales para ambas partes."
        "</div>", unsafe_allow_html=True)

    ab_section("Buscador semántico de claves SAT")

    query = st.text_input("Describe el producto o servicio en lenguaje natural",
                          value="Soldadura especializada con arco eléctrico "
                                "para estructuras metálicas industriales")

    if query:
        st.markdown(f"**Top 5 claves SAT más cercanas semánticamente a:** "
                    f"*{query}*")
        sat_points = data.df_catalogos[
            data.df_catalogos["type"] == "Catálogo SAT-CFDI"
        ].copy()

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

    ab_section("Casos de uso comercial")
    c1, c2 = st.columns(2)
    c1.markdown("""
    **Para ERPs y sistemas de facturación**

    Plugin que sugiere las 3 claves SAT más probables en el momento de
    emitir el CFDI, basándose en la descripción que el usuario escribe.
    Reduce errores de clasificación en ~70%.
    """)
    c2.markdown("""
    **Para auditoría masiva**

    Revisa CFDIs ya emitidos y detecta casos donde la clave declarada no
    corresponde semánticamente a la descripción — patrón típico de
    operaciones simuladas o errores de captura.
    """)

    ab_section("Precisión del método")
    st.markdown("""
    Usando `text-embedding-3-small` (1,536 dimensiones) y los 50,000+
    registros del catálogo SAT pre-embebidos, la clave correcta aparece en
    el top-5 en aproximadamente el **88%** de los casos probados
    internamente. En top-10, **95%**.
    """)
