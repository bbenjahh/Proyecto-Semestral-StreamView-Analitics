# Proyecto de Visualización de Datos: StreamView Analytics (EP5)

**Asignatura:** Visualización de Datos (`ADY1104`) — Duoc UC  
**Equipo Consultor:** Benjamín Patiño & Benjamín Vargas  
**Cliente:** StreamView Analytics  

---

## 1. Descripción del Proyecto
Solución integral de analítica y comunicación visual diseñada para responder al desafío de retención de usuarios en los primeros 90 días (*Churn Rate* del 18%) y optimizar el nivel de interacción (*Engagement*) del catálogo global de **StreamView Analytics** (31.594 títulos únicos entre 2010 y 2025).

La solución aplica principios de percepción visual (Cleveland & McGill, leyes de la Gestalt), reducción de carga cognitiva y accesibilidad cromática universal (**paleta Okabe-Ito**: Azul Petróleo `#005f73` para Series y Ámbar `#ee9b00` para Películas).

---

## 2. Estructura Profesional del Proyecto

```text
StreamView_Analytics_EP5/
│
├── dashboard/
│   └── app.py                                     # Aplicación interactiva en Dash / Plotly
│
├── data/
│   ├── netflix_movies_detailed_up_to_2025.csv     # Fuente corporativa Películas (16.000 registros)
│   ├── netflix_tv_shows_detailed_up_to_2025.csv   # Fuente corporativa Series (16.000 registros)
│   └── streamview_master_processed.csv            # Dataset maestro limpio (31.594 registros únicos)
│
├── images/                                        # Capturas estáticas de apoyo para presentaciones
│   ├── fig1_evolucion_catalogo.png                 # Evolución de volumen y popularidad (2010-2025)
│   ├── fig2_popularidad_generos.png                # Engagement promedio en el Top 10 de géneros
│   ├── fig3_matriz_calidad_popularidad.png         # Matriz estratégica Calificación vs. Popularidad
│   └── fig4_heatmap_mercados_generos.png           # Mapa de calor por País Productor y Género
│
├── notebooks/
│   └── Proyecto_Semestral_StreamViewAnalitics_EP5_Final.ipynb # Notebook de exploración (EDA) y prototipado
│
├── src/
│   └── data_processing.py                         # Pipeline reproducible de limpieza e integración
│
├── Informe Ejecutivo StreamView Analytics.pdf     # Entregable 1: Informe Ejecutivo detallado
├── README.md                                      # Documentación y guía de reproducción
└── Resumen Ejecutivo StreamView Analytics.pdf     # Entregable 3: Resumen Ejecutivo directivo
```

---

## 3. Instrucciones de Instalación y Ejecución

### Requisitos Previos
* Python 3.10 o superior.
* Ubicarse en la **carpeta raíz** del proyecto desde la terminal e instalar las dependencias necesarias:

```bash
pip install pandas numpy plotly dash matplotlib seaborn nbformat
```

### Paso 1: Ejecutar el Pipeline de Datos (Opcional)
Para verificar la limpieza y generar el archivo consolidado `streamview_master_processed.csv`:

```bash
python src/data_processing.py
```

### Paso 2: Iniciar el Dashboard Interactivo
Para levantar el servidor local de Dash:

```bash
python dashboard/app.py
```
Luego abre en tu navegador `http://127.0.0.1:8050/`. Si deseas ejecutarlo directamente dentro de una celda de **Google Colab**, reemplaza la última línea de `dashboard/app.py` por `app.run(jupyter_mode="inline", port=8050)`.