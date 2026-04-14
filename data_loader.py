"""
data_loader.py — generación de datos ficticios para el demo

Empresa ficticia: MetalTécnica del Centro, S.A. de C.V.
Sector inventado: metal-mecánica (estructuras, herrería, maquinaria).

Los puntos del caso están deliberadamente diseñados para contar cuatro
historias de riesgo en la junta:

  A) Objeto social vs. CFDI — 3 conceptos muy alejados del núcleo del
     acta (consultoría estratégica, licenciamiento de software, mkt digital)
     por un total de $12.4M, fuera del objeto social metal-mecánico.

  B) REPSE "fantasma" — un proveedor que factura limpieza industrial
     bajo un registro REPSE cuyo alcance original es solo vigilancia
     privada. Mismatch semántico grave.

  C) Partes relacionadas — 3 CFDIs con descripciones vagas
     ("servicios administrativos varios") por $8.7M al mismo receptor,
     muy lejos del núcleo del acta.

  D) CSF desactualizada — la CSF declara solo "fabricación de
     estructuras metálicas" pero hay $14.3M facturados en instalación
     eléctrica y obra civil.
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd
import streamlit as st


CATALOG_TYPES = [
    "Catálogo de Productos",
    "Catálogo de Actividades-Productos",
    "Catálogo SAT-CFDI",
]

CASE_TYPES = [
    "Productos Fuera de REPSE (Emitidos)",
    "Productos Dentro de REPSE (Emitidos)",
    "Productos Fuera de REPSE (Recibidos)",
    "Productos Dentro de REPSE (Recibidos)",
    "Actividad CSF",
    "Texto del Acta",
]


# --------------------------------------------------------------------
@dataclass
class DemoData:
    df_catalogos: pd.DataFrame          # universo semántico de referencia
    df_caso: pd.DataFrame               # caso MetalTécnica
    df_all: pd.DataFrame                # ambos concatenados
    cfdi_summary: pd.DataFrame
    key_findings: dict


# --------------------------------------------------------------------
# SIMULACIÓN
# --------------------------------------------------------------------
def _simulate_catalog(n: int, center: np.ndarray, spread: float, cat_type: str,
                      rng: np.random.Generator) -> pd.DataFrame:
    pts = rng.normal(loc=center, scale=spread, size=(n, 3))
    pts += rng.normal(0, spread * 0.3, size=(n, 3)) ** 3 * 0.1

    sample_texts = {
        "Catálogo de Productos": [
            "Estructuras metálicas soldadas para uso industrial",
            "Herrajes de acero para construcción",
            "Maquinaria de corte CNC",
            "Perfiles de aluminio anodizado",
            "Servicios de galvanizado en caliente",
            "Tornillería y sujetadores industriales",
            "Equipos de soldadura por arco",
        ],
        "Catálogo de Actividades-Productos": [
            "Fabricación de productos metálicos bajo pedido",
            "Reparación de equipo industrial pesado",
            "Mantenimiento preventivo de maquinaria",
            "Instalación de estructuras metálicas en obra",
            "Servicios especializados de maquila metal-mecánica",
        ],
        "Catálogo SAT-CFDI": [
            "Servicios de herrería",
            "Fabricación de herramientas manuales",
            "Servicios de mantenimiento industrial",
            "Productos metálicos diversos",
            "Servicios profesionales de ingeniería mecánica",
            "Maquila de corte y soldadura",
        ],
    }
    texts = rng.choice(sample_texts[cat_type], size=n, replace=True)

    return pd.DataFrame({
        "type": cat_type,
        "text": texts,
        "PCA1": pts[:, 0],
        "PCA2": pts[:, 1],
        "PCA3": pts[:, 2],
        "clave_prod_serv": [f"{rng.integers(10000000, 99999999)}" for _ in range(n)],
    })


def _simulate_case(rng: np.random.Generator) -> pd.DataFrame:
    """
    Construye el perfil semántico ficticio de MetalTécnica del Centro
    con hallazgos de riesgo plantados deliberadamente.
    """
    rows = []
    acta_center = np.array([0.25, 0.10, -0.05])

    # ------------------------------------------------------------
    # 1) TEXTO DEL ACTA — 4 finalidades en zona metal-mecánica
    # ------------------------------------------------------------
    acta_texts = [
        "Fabricación, comercialización e instalación de estructuras metálicas",
        "Reparación y mantenimiento de maquinaria y equipo industrial",
        "Compra-venta de materiales ferrosos y no ferrosos",
        "Servicios de herrería artística y arquitectónica",
    ]
    for txt in acta_texts:
        p = acta_center + rng.normal(0, 0.04, 3)
        rows.append({"type": "Texto del Acta", "text": txt,
                     "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": None, "importe": None,
                     "contraparte": None, "risk_tag": None})

    # ------------------------------------------------------------
    # 2) ACTIVIDAD CSF — *desactualizada*: solo estructuras metálicas
    #    No declara instalación eléctrica ni obra civil (hallazgo D)
    # ------------------------------------------------------------
    csf_texts = [
        "Fabricación de estructuras metálicas y productos de herrerías",
    ]
    for txt in csf_texts:
        p = acta_center + rng.normal(0, 0.04, 3)
        rows.append({"type": "Actividad CSF", "text": txt,
                     "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": None, "importe": None,
                     "contraparte": None, "risk_tag": None})

    # ------------------------------------------------------------
    # 3) EMITIDOS DENTRO REPSE — servicios especializados coherentes
    # ------------------------------------------------------------
    for _ in range(14):
        p = acta_center + rng.normal(0, 0.08, 3)
        rows.append({"type": "Productos Dentro de REPSE (Emitidos)",
                     "text": rng.choice([
                         "Servicios especializados de soldadura",
                         "Maquila de corte láser",
                         "Servicios de pintura industrial",
                         "Ensamble de estructuras metálicas",
                         "Servicios de armado en planta",
                     ]),
                     "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": f"8111{rng.integers(1000, 9999)}",
                     "importe": float(rng.integers(80000, 900000)),
                     "contraparte": f"Cliente {rng.integers(100, 999)}",
                     "risk_tag": None})

    # ------------------------------------------------------------
    # 4) EMITIDOS FUERA REPSE — la parte operativa normal
    # ------------------------------------------------------------
    for _ in range(20):
        p = acta_center + rng.normal(0, 0.09, 3)
        rows.append({"type": "Productos Fuera de REPSE (Emitidos)",
                     "text": rng.choice([
                         "Estructura metálica terminada",
                         "Herrajes fabricados bajo pedido",
                         "Piezas de acero cortadas a medida",
                         "Perfiles estructurales",
                         "Racks industriales",
                     ]),
                     "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": f"301015{rng.integers(10, 99)}",
                     "importe": float(rng.integers(150000, 1800000)),
                     "contraparte": f"Cliente {rng.integers(100, 999)}",
                     "risk_tag": None})

    # ------------------------------------------------------------
    # HALLAZGO A · OBJETO SOCIAL vs. CFDI — 3 outliers muy lejos
    # ------------------------------------------------------------
    hallazgo_A = [
        (np.array([-0.50, 0.38, 0.30]),
         "Servicios de consultoría estratégica y planeación corporativa",
         "80101500", 6_200_000.0, "Cliente 4471",
         "objeto_social"),
        (np.array([-0.38, -0.48, 0.35]),
         "Licenciamiento anual de software empresarial",
         "81112200", 4_800_000.0, "Cliente 2183",
         "objeto_social"),
        (np.array([0.12, 0.45, 0.42]),
         "Servicios integrales de publicidad y marketing digital",
         "82101500", 1_400_000.0, "Cliente 6620",
         "objeto_social"),
    ]
    for p, txt, clave, imp, cp, tag in hallazgo_A:
        rows.append({"type": "Productos Fuera de REPSE (Emitidos)",
                     "text": txt, "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": clave, "importe": imp,
                     "contraparte": cp, "risk_tag": tag})

    # ------------------------------------------------------------
    # HALLAZGO C · PARTES RELACIONADAS — 3 CFDIs vagos mismo receptor
    # ------------------------------------------------------------
    hallazgo_C = [
        (np.array([-0.25, 0.30, -0.35]),
         "Servicios administrativos varios",
         "84111500", 3_200_000.0, "Cliente 9001",
         "partes_relacionadas"),
        (np.array([-0.28, 0.28, -0.38]),
         "Servicios administrativos varios",
         "84111500", 2_900_000.0, "Cliente 9001",
         "partes_relacionadas"),
        (np.array([-0.22, 0.33, -0.32]),
         "Servicios administrativos varios",
         "84111500", 2_600_000.0, "Cliente 9001",
         "partes_relacionadas"),
    ]
    for p, txt, clave, imp, cp, tag in hallazgo_C:
        rows.append({"type": "Productos Fuera de REPSE (Emitidos)",
                     "text": txt, "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": clave, "importe": imp,
                     "contraparte": cp, "risk_tag": tag})

    # ------------------------------------------------------------
    # HALLAZGO D · CSF DESACTUALIZADA — $14.3M en instalación eléctrica
    #     y obra civil, actividades NO declaradas en CSF
    # ------------------------------------------------------------
    hallazgo_D = [
        (np.array([0.05, -0.35, 0.15]),
         "Instalaciones eléctricas industriales",
         "72101500", 5_100_000.0, "Cliente 3344",
         "csf_desactualizada"),
        (np.array([0.08, -0.38, 0.12]),
         "Obra civil y cimentaciones",
         "72141100", 6_200_000.0, "Cliente 2255",
         "csf_desactualizada"),
        (np.array([0.02, -0.32, 0.18]),
         "Montaje de tableros de control eléctrico",
         "72151500", 3_000_000.0, "Cliente 3344",
         "csf_desactualizada"),
    ]
    for p, txt, clave, imp, cp, tag in hallazgo_D:
        rows.append({"type": "Productos Fuera de REPSE (Emitidos)",
                     "text": txt, "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": clave, "importe": imp,
                     "contraparte": cp, "risk_tag": tag})

    # ------------------------------------------------------------
    # HALLAZGO B · REPSE FANTASMA — proveedor REPSE que factura
    #   servicios de limpieza pero su alcance registrado es vigilancia
    # ------------------------------------------------------------
    # "Dentro de REPSE (Recibidos)" pero semánticamente desalineado
    hallazgo_B = [
        (np.array([-0.42, -0.15, -0.40]),
         "Servicios de limpieza industrial profunda",
         "76111500", 1_800_000.0, "Proveedor REPSE 8812",
         "repse_fantasma"),
        (np.array([-0.38, -0.18, -0.42]),
         "Servicios de limpieza y mantenimiento de pisos",
         "76111501", 1_100_000.0, "Proveedor REPSE 8812",
         "repse_fantasma"),
    ]
    for p, txt, clave, imp, cp, tag in hallazgo_B:
        rows.append({"type": "Productos Dentro de REPSE (Recibidos)",
                     "text": txt, "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": clave, "importe": imp,
                     "contraparte": cp, "risk_tag": tag})

    # ------------------------------------------------------------
    # 5) RECIBIDOS FUERA REPSE — normal, proveedores diversos
    # ------------------------------------------------------------
    for _ in range(28):
        p = rng.normal(0, 0.35, 3)
        rows.append({"type": "Productos Fuera de REPSE (Recibidos)",
                     "text": rng.choice([
                         "Lámina de acero al carbono",
                         "Energía eléctrica industrial",
                         "Servicios de telefonía empresarial",
                         "Refacciones industriales",
                         "Material de oficina",
                         "Combustible diésel",
                         "Equipos de cómputo",
                         "Servicios de mensajería",
                     ]),
                     "PCA1": p[0], "PCA2": p[1], "PCA3": p[2],
                     "clave_prod_serv": f"{rng.integers(10000000, 99999999)}",
                     "importe": float(rng.integers(15000, 600000)),
                     "contraparte": f"Proveedor {rng.integers(100, 999)}",
                     "risk_tag": None})

    return pd.DataFrame(rows)


def _simulate_all(seed: int = 42) -> DemoData:
    rng = np.random.default_rng(seed)

    cat_dfs = [
        _simulate_catalog(800, np.array([0.0, 0.0, 0.0]), 0.35,
                          "Catálogo de Productos", rng),
        _simulate_catalog(600, np.array([0.05, 0.02, 0.0]), 0.32,
                          "Catálogo de Actividades-Productos", rng),
        _simulate_catalog(900, np.array([-0.02, 0.03, 0.01]), 0.38,
                          "Catálogo SAT-CFDI", rng),
    ]
    df_catalogos = pd.concat(cat_dfs, ignore_index=True)
    df_caso = _simulate_case(rng)
    df_all = pd.concat([df_catalogos, df_caso], ignore_index=True)

    # Resumen de flujos
    def _sum_by(t):
        sub = df_caso[df_caso["type"] == t]
        return int(len(sub)), float(sub["importe"].sum() if "importe" in sub else 0)

    flujos = [
        ("Emitidos DENTRO REPSE", "Productos Dentro de REPSE (Emitidos)"),
        ("Emitidos FUERA REPSE",  "Productos Fuera de REPSE (Emitidos)"),
        ("Recibidos DENTRO REPSE","Productos Dentro de REPSE (Recibidos)"),
        ("Recibidos FUERA REPSE", "Productos Fuera de REPSE (Recibidos)"),
    ]
    cfdi_summary = pd.DataFrame([
        {"Flujo": label, "CFDIs": _sum_by(t)[0], "Importe (MXN)": _sum_by(t)[1]}
        for label, t in flujos
    ])

    # Hallazgos ya marcados con risk_tag
    hallazgos_A = df_caso[df_caso["risk_tag"] == "objeto_social"].copy()
    hallazgos_B = df_caso[df_caso["risk_tag"] == "repse_fantasma"].copy()
    hallazgos_C = df_caso[df_caso["risk_tag"] == "partes_relacionadas"].copy()
    hallazgos_D = df_caso[df_caso["risk_tag"] == "csf_desactualizada"].copy()

    acta_center = np.array([0.25, 0.10, -0.05])

    def _add_dist(df):
        if df.empty:
            return df
        df = df.copy()
        df["dist_acta"] = np.sqrt(
            (df["PCA1"] - acta_center[0]) ** 2 +
            (df["PCA2"] - acta_center[1]) ** 2 +
            (df["PCA3"] - acta_center[2]) ** 2
        )
        return df

    key_findings = {
        "acta_center": acta_center,
        "hallazgos_A": _add_dist(hallazgos_A),   # objeto social
        "hallazgos_B": _add_dist(hallazgos_B),   # repse fantasma
        "hallazgos_C": _add_dist(hallazgos_C),   # partes relacionadas
        "hallazgos_D": _add_dist(hallazgos_D),   # csf desactualizada
        "distancia_max_universo": 1.1628,
        "distancia_max_caso": 0.9707,
        "total_outliers_monto": float(
            hallazgos_A["importe"].sum() + hallazgos_C["importe"].sum()
            + hallazgos_D["importe"].sum()
        ),
    }

    return DemoData(df_catalogos=df_catalogos, df_caso=df_caso,
                    df_all=df_all, cfdi_summary=cfdi_summary,
                    key_findings=key_findings)


@st.cache_data(show_spinner="Generando universo semántico…")
def load_data() -> DemoData:
    return _simulate_all()
