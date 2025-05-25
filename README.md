# Proyecto Integrado V - Grupo Aval Tracker (AVAL)

Este proyecto tiene como objetivo automatizar la recolección continua de datos históricos del **Grupo Aval (AVAL)**, una de las principales entidades financieras de Colombia. Los datos se obtienen desde **Yahoo Finanzas**, se almacenan en formato `.csv` y se actualizan automáticamente mediante **GitHub Actions**, manteniendo la trazabilidad y persistencia del histórico.

---

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

---

## ⚙️ Tecnologías utilizadas

- Python 3.10
- [yfinance](https://pypi.org/project/yfinance/)
- pandas
- logging
- GitHub Actions

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
   GitHub ejecuta el flujo `.github/workflows/update_data.yml` diariamente a las 12:00 UTC.  
   Los datos se actualizan en `historical.csv`, los logs detallados se guardan en `text_logs/` y el resumen tabular en `log_data.csv`.

---

## 🌐 Dashboard interactivo

Puedes consultar el análisis y visualización de los datos en el siguiente enlace a la aplicación desplegada en Streamlit Cloud:

[https://proyectointegradovavaltracker.streamlit.app/](https://proyectointegradovavaltracker.streamlit.app/)

---

## 📄 Licencia

Este proyecto es de uso educativo y forma parte de la asignatura **Proyecto Integrado V**, bajo la línea de énfasis en automatización y análisis económico.

---