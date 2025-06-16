# Grupo Aval Tracker - Análisis Financiero Automatizado

**Grupo Aval Tracker** es una solución profesional desarrollada para automatizar el análisis histórico, técnico y predictivo de las acciones del Grupo Aval (AVAL), el conglomerado financiero más grande de Colombia. Integra recolección diaria de datos, enriquecimiento con indicadores bursátiles, modelado ARIMA y visualización en un dashboard interactivo.

---

## 📌 Características

- 🔄 **Automatización diaria con GitHub Actions** (4:10 p.m. hora Colombia)
- 📋 **Registro de logs**: trazabilidad completa por ejecución (`log_data.csv`, archivos .log)
- 📊 **Indicadores técnicos incluidos**: RSI, SMA21/50, Bandas de Bollinger, Volatilidad, Retorno acumulado
- 🤖 **Modelo predictivo ARIMA (3,1,1)** con R² = 0.921
- 📈 **Visualización interactiva**: dashboard en Streamlit Cloud
- 📦 **Distribución como paquete** vía `setup.py`

---

## 🔍 Justificación del modelo ARIMA

- **ARIMA(3,1,1)** fue seleccionado tras evaluación por AIC y comparativa con SARIMA.
- Mostró mejor desempeño en predicción:
  - **MAE**: 7.83
  - **RMSE**: 11.14
  - **MAPE**: 2.48%
  - **R²**: 0.921

---

## 📈 Indicador económico

- **Activo**: Grupo Aval Acciones y Valores S.A.
- **Símbolo bursátil**: `AVAL`
- [🔗 Ver en Yahoo Finanzas](https://es-us.finanzas.yahoo.com/quote/AVAL/)

---

## 🌐 Dashboard interactivo

Consulta el dashboard actualizado con visualización de indicadores y predicción en:

[https://proyectointegradovavaltracker.streamlit.app/](https://proyectointegradovavaltracker.streamlit.app/)

---

## 🎥 Presentación profesional del proyecto

Mira la presentación oficial donde se explica la estructura, funcionamiento y resultados:

[🔗 Ver presentación en video](https://drive.google.com/file/d/1ZQWDnACqp1Gk2em9FfcXzz530FjJtNVz/view?usp=sharing)

---

## ⚙️ Tecnologías utilizadas

- Python 3.10
- yfinance, pandas, numpy, statsmodels, plotly, scikit-learn
- logging, GitHub Actions
- Streamlit / Streamlit Cloud

---

## 📁 Estructura del repositorio

```
proyecto_integrado_v_aval_tracker/
├── .github/
│   └── workflows/
│       └── update_data.yml               # GitHub Actions workflow para actualización automática
│
├── docs/
│   └── report_entrega1.pdf               # Primer Informe en formato APA
│   └── report_final.pdf                  # Informe Final en formato APA
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

### Instalación local
```bash
pip install -r requirements.txt
```

### Ejecutar colector localmente
```bash
python src/collector.py
```

### Automatización con GitHub Actions
El flujo `.github/workflows/update_data.yml` se ejecuta automáticamente cada día a las 21:10 UTC (4:10 p.m. Colombia), actualizando:
- `historical.csv`
- `log_data.csv`
- Archivos .log en `text_logs/`

---

## 📌 Estado del desarrollo

- [x] Automatización completa y logging
- [x] Recolección y enriquecimiento de datos
- [x] Modelo ARIMA funcional con métricas
- [x] Visualización en Streamlit Cloud
- [ ] Autenticación privada (pendiente)
- [ ] Evaluación de modelos LSTM/Prophet (en planificación)

---

## 📄 Licencia

Este proyecto es de uso profesional y está orientado a analistas financieros, desarrolladores fintech y equipos técnicos que requieran análisis continuo y automatizado de activos bursátiles.