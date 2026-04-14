# analítica boutique · demo

**Análisis semántico de riesgo fiscal y regulatorio**

App Streamlit para presentar a clientes potenciales el procedimiento de
análisis por embeddings + PCA + convex hull, estructurado como cinco
casos de aplicación comercial.

Respeta el *Manual de Identidad Corporativa* de Analítica Boutique:

- azul corporativo `#3C4981` (Pantone 280 U)
- naranja acento `#EE7F4B` (Pantone 158 U) — *"el punto"*
- **Century Gothic** para títulos (fallback web: Questrial)
- **Calibri** para cuerpo de texto (fallback web: Lato)

---

## Qué incluye

Una sola app con seis pestañas:

| # | Pestaña | Ángulo de venta |
|---|---|---|
| 0 | visión general | El método y el pipeline, en 4 pasos |
| 1 | riesgo REPSE | Cobertura semántica del registro vs. facturación real |
| 2 | objeto social vs. CFDI | Detección de outliers fuera del acta |
| 3 | KYC de proveedores | Due diligence automatizado pre-contratación |
| 4 | auditoría asistida | Del día-hombre a la hora-hombre |
| 5 | clasificación SAT | Buscador semántico de claves |

---

## Caso ficticio: MetalTécnica del Centro, S.A. de C.V.

**Todos los datos del demo son ficticios.** La empresa "MetalTécnica del
Centro" no existe; cualquier similitud con una organización real es
coincidencia.

Los datos están construidos para contar cuatro historias de riesgo
contundentes en la junta:

| # | Hallazgo | Monto | Severidad |
|---|---|---:|---|
| **A** | Conceptos facturados fuera del objeto social (consultoría, software, marketing) | $12.4M | Alta |
| **B** | REPSE "fantasma": proveedor factura limpieza pero su alcance es vigilancia | $2.9M | Alta |
| **C** | Partes relacionadas: 3 CFDIs idénticos y vagos al mismo receptor | $8.7M | Alta |
| **D** | CSF desactualizada: $14.3M en actividades eléctrica y obra civil no declaradas | $14.3M | Alta |


## Guion sugerido para la junta (15 min)

**Minuto 0–2 · Gancho (Tab "visión general")**
> "Hoy, cuando una empresa emite 90,000 facturas al año, nadie verifica que
> coincidan con lo que dice su acta y su CSF. Les voy a mostrar cómo verlo."

Muestra el mapa 3D completo. Rota la cámara. Señala:
- La nube tenue de fondo → "todo lo que el SAT conoce"
- Los puntos brillantes → "la huella semántica de MetalTécnica"
- Los puntos naranjas → "CFDIs emitidos fuera de REPSE, donde están las alertas"

**Minuto 2–5 · Tab ① riesgo REPSE**
Aquí entra el **hallazgo B** (REPSE fantasma). Es el más técnico pero el
más contundente para audiencia fiscal/compliance.
> "Este proveedor tiene REPSE vigente. Pero su registro cubre vigilancia
> privada, y le facturó a MetalTécnica $2.9M por limpieza industrial.
> ¿Se deduce o no?"

**Minuto 5–9 · Tab ② objeto social vs. CFDI**
Tu historia estrella: **hallazgos A y C** juntos.
> "Estos tres conceptos, $12.4M, no caen dentro del objeto social. Ningún
> humano encontraría esto leyendo facturas."
> "Y miren este otro patrón: tres facturas, misma descripción, mismo
> cliente, $8.7M. El embedding las agrupa automáticamente."

**Minuto 9–11 · Tab ③ KYC**
Cambia de "revisión propia" a "revisión de terceros". Abre conversación
con el área de compras/cumplimiento del cliente.

**Minuto 11–13 · Tab ④ auditoría asisida**
Muestra el ranking completo de 6 hallazgos y la tabla de tiempos
(3-5 días vs <30 min). Es el cierre comercial.

**Minuto 13–14 · Tab ⑤ clasificación SAT**
Bonus rápido. Demuestra la extensibilidad del método.

**Minuto 14–15 · Preguntas + siguientes pasos**


## Estructura del proyecto

```
demo_repse/
├── app.py              # punto de entrada Streamlit
├── branding.py         # paleta, CSS, logo SVG
├── data_loader.py      # simulación de MetalTécnica del Centro
├── views.py            # una función por tab (narrativa del demo)
├── requirements.txt
└── README.md
```
