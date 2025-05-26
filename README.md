# Proyecto Integrado V - Grupo Aval Tracker (AVAL)

Este proyecto tiene como objetivo automatizar la recolección continua de datos históricos del **Grupo Aval (AVAL)**, una de las principales entidades financieras de Colombia. Los datos se obtienen desde **Yahoo Finanzas**, se almacenan en formato `.csv` y se actualizan automáticamente mediante **GitHub Actions**, manteniendo la trazabilidad y persistencia del histórico.

---

## 📌 Características

- 🔄 **Automatización diaria con GitHub Actions**: Los datos se actualizan automáticamente cada día a las 21:10 UTC (4:10 p.m. Colombia).  
- 📊 **Almacenamiento histórico en CSV**: Los datos se mantienen en formato CSV para facilitar su análisis.  
- 🧾 **Sistema dual de logging**:  
  - 📁 Archivos `.log` por ejecución en `text_logs/`, con registros detallados y timestamp.  
  - 📋 Archivo `log_data.csv` estructurado, útil para análisis tabular y trazabilidad resumida, gestionado por `csv_logger.py`.  
- 🧱 **Implementación con Programación Orientada a Objetos (OOP)**: El código se organiza utilizando principios de OOP.  
- 🧪 **Recolector de datos con `yfinance` y `pandas`**: Descarga automática desde Yahoo Finanzas.  
- 📈 **Enriquecimiento de datos con indicadores técnicos y KPIs**: Cálculo automático de medias móviles, RSI, bandas de Bollinger, volatilidad, momentum, entre otros, mediante `enricher.py`.  
- 🤖 **Modelado y predicción con ARIMA**: Implementación del modelo ARIMA para análisis de series temporales y predicción, gestionado en `arima_model.py` y almacenado en la carpeta `models/`.  
- 📊 **Dashboard interactivo con Streamlit**: Visualización dinámica y análisis de datos históricos, indicadores y predicciones en `dashboard.py`.  
- 📦 **Distribución del paquete con `setup.py`**: Estructura lista para instalación local/remota como paquete Python.

---
## Justificación de la elección del modelo ARIMA y métricas de evaluación

### Elección del modelo ARIMA

Para la predicción de la serie temporal de precios ajustados de la acción Grupo Aval (AVAL), se seleccionó el modelo ARIMA debido a su capacidad probada para modelar series temporales financieras con tendencias y patrones autoregresivos.

Inicialmente se evaluó un modelo SARIMA que incluye diferenciación estacional para capturar posibles patrones anuales. Sin embargo, este modelo presentó mucho ruido y un desempeño inferior, por lo que se optó por un modelo ARIMA sin componente estacional.

Se utilizó un proceso automático de búsqueda paso a paso (stepwise) para identificar el modelo ARIMA que minimiza el criterio de información de Akaike (AIC), un indicador que balancea la calidad del ajuste con la complejidad del modelo. Durante esta búsqueda, se evaluaron múltiples configuraciones de parámetros (p, d, q), incluyendo modelos con y sin intercepto.

El mejor modelo encontrado fue ARIMA(3,1,1), con parámetros:

- **p=3**: tres rezagos en la parte autoregresiva,
- **d=1**: una diferenciación para hacer la serie estacionaria,
- **q=1**: un término de promedio móvil de orden 1.

Este modelo obtuvo el menor valor de AIC, indicando el mejor balance entre ajuste y parsimonia, y mostró un buen desempeño en la predicción de la serie.

### Comparación con modelo SARIMA

Se comparó el modelo ARIMA con un modelo SARIMA que incluye estacionalidad anual. Los resultados mostraron que el modelo ARIMA tuvo un mejor desempeño, con menor error (RMSE = 11.14 vs 14.57) y mejor ajuste (R² = 0.921 vs 0.881), lo que justifica la elección de ARIMA sin componente estacional para este caso.

### Justificación de las métricas de evaluación

Para evaluar el desempeño del modelo ARIMA se seleccionaron las siguientes métricas:

- **MAE (Error Absoluto Medio):** Mide el error promedio en las unidades originales, facilitando la interpretación directa del desempeño del modelo. Es menos sensible a errores extremos, lo que es útil en series financieras con fluctuaciones moderadas.

- **RMSE (Raíz del Error Cuadrático Medio):** Penaliza más fuertemente los errores grandes, permitiendo identificar desviaciones significativas en las predicciones que podrían afectar decisiones financieras.

- **MAPE (Error Porcentual Absoluto Medio):** Expresa el error en términos porcentuales, facilitando la comparación relativa del desempeño del modelo en diferentes períodos o activos.

- **R² (Coeficiente de Determinación):** Indica la proporción de la variabilidad de los datos que es explicada por el modelo, proporcionando una medida global de ajuste y capacidad predictiva.

La combinación de estas métricas permite una evaluación integral del modelo, considerando tanto la magnitud absoluta de los errores como su impacto relativo y la capacidad explicativa del modelo. Esto es especialmente relevante en el contexto financiero, donde tanto la precisión como la confiabilidad de las predicciones son críticas para la toma de decisiones.

---

## ⚙️ Tecnologías utilizadas

- Python 3.10  
- [yfinance](https://pypi.org/project/yfinance/) — para descarga de datos financieros  
- pandas — manipulación y análisis de datos  
- logging — gestión de logs  
- GitHub Actions — automatización y despliegue continuo  
- [Streamlit](https://streamlit.io/) — creación de dashboard interactivo para visualización de datos  
- Streamlit Cloud — plataforma para despliegue y hosting del dashboard  

---

## 📈 Indicador económico

- **Activo**: Grupo Aval Acciones y Valores S.A.
- **Símbolo**: `AVAL`
- [🔗 Ver en Yahoo Finanzas](https://es-us.finanzas.yahoo.com/quote/AVAL/)

---

## 📁 Estructura del repositorio

```
proyecto_integrado_v_aval_tracker/
├── .github/
│   └── workflows/
│       └── update_data.yml               # GitHub Actions workflow para actualización automática
│
├── docs/
│   └── report_entrega1.pdf               # Informe en formato APA
│
├── src/
│   ├── arima_model.py                       # Modelado y predicción (ML, ARIMA, etc.)
│   ├── collector.py                      # Script para recolección de datos
│   ├── csv_logger.py                     # Logger para logs en formato CSV
│   ├── dashboard.py                      # Dashboard interactivo con Streamlit
│   ├── enricher.py                       # Enriquecimiento de datos con indicadores técnicos
│   ├── logger.py                         # Logger general para archivos .log
│   ├── models/                           # Carpeta para almacenar modelos y métricas
│   │   ├── arima_metrics.csv             # Métricas del modelo ARIMA
│   │   └── arima_model.pkl               # Modelo ARIMA serializado
│   └── static/
│       └── data/
│           ├── enriched_historical.csv  # Datos históricos enriquecidos con indicadores
│           └── historical.csv           # Datos históricos originales
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 Instrucciones de uso

1. **Instala dependencias**:

   ```bash
   pip install yfinance pandas
   ```

2. **Ejecuta el colector localmente**:

   ```bash
   python src/collector.py
   ```

3. **Automatización con GitHub Actions**:  
   GitHub ejecuta el flujo `.github/workflows/update_data.yml` diariamente a las 21:10 UTC (4:10 p.m. Colombia).  
   Los datos se actualizan en `historical.csv`, los logs detallados se guardan en `text_logs/` y el resumen tabular en `log_data.csv`.

---

## 🌐 Dashboard interactivo

Puedes consultar el análisis y visualización de los datos en el siguiente enlace a la aplicación desplegada en Streamlit Cloud:

[https://proyectointegradovavaltracker.streamlit.app/](https://proyectointegradovavaltracker.streamlit.app/)

---

## 📄 Licencia

Este proyecto es de uso educativo y forma parte de la asignatura **Proyecto Integrado V**, bajo la línea de énfasis en automatización y análisis económico.

---