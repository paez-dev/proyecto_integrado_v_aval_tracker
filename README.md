## Proyecto Integrado V - Grupo Aval Tracker (AVAL)

Este proyecto tiene como objetivo automatizar la recolección continua de datos históricos del **Grupo Aval (AVAL)**, 
una de las principales entidades financieras de Colombia. Los datos se obtienen desde **Yahoo Finanzas**, 
se almacenan en formato `.csv` y se actualizan automáticamente mediante **GitHub Actions**, manteniendo 
la trazabilidad y persistencia del histórico.

## 📌 Características

* 🔄 **Automatización diaria con GitHub Actions**: Los datos se actualizan automáticamente cada día a las 12:00 UTC.
* 📊 **Almacenamiento histórico en `CSV`**: Los datos se mantienen en formato CSV para facilitar su análisis.
* 🧾 **Sistema dual de logging**:

  * 📁 Archivos `.log` por ejecución en `text_logs/`, con registros detallados y timestamp.
  * 📋 Archivo `log_data.csv` estructurado, útil para análisis tabular y trazabilidad resumida, gestionado por `csv_logger.py`.
* 🧱 **Implementación con Programación Orientada a Objetos (OOP)**: El código se organiza utilizando principios de OOP.
* 🧪 **Recolector de datos con `yfinance` y `pandas`**: Descarga automática desde Yahoo Finanzas.
* 📦 **Distribución del paquete con `setup.py`**: Estructura lista para instalación local/remota como paquete Python.

## ⚙️ Tecnologías utilizadas

* Python 3.10
* [yfinance](https://pypi.org/project/yfinance/)
* pandas
* logging
* GitHub Actions

## 📈 Indicador económico

* **Activo**: Grupo Aval Acciones y Valores S.A.
* **Símbolo**: `AVAL`
* [🔗 Ver en Yahoo Finanzas](https://es-us.finanzas.yahoo.com/quote/AVAL/)

## 📁 Estructura del repositorio

```
proyecto_integrado_v_aval_tracker/
├── .github/
│   └── workflows/
│       └── update_data.yml          # Flujo automático con GitHub Actions
│
├── docs/
│   └── report_entrega1.pdf          # Informe en formato APA
│
├── src/
│   ├── collector.py                 # Script principal de recolección de datos
│   ├── logger.py                    # Logger general (.log)
│   ├── csv_logger.py                # Logger estructurado (log_data.csv)
│   ├── static/
│   │   └── data/
│   │       └── historical.csv       # Archivo CSV con datos históricos actualizados
│   └── logs/
│       ├── log_data.csv             # Log central en formato CSV
│       └── text_logs/
│           └── aval_analysis_YYYYMMDD_HHMMSS.log  # Logs detallados por ejecución
│
├── setup.py                         # Script de instalación como paquete
├── README.md
└── .gitignore
```

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
   Los datos se actualizan en `historical.csv`, los logs detallados se guardan en `text_logs/`
   y el resumen tabular en `log_data.csv`.

## 📄 Licencia

Este proyecto es de uso educativo y forma parte de la asignatura **Proyecto Integrado V**, bajo la línea de 
énfasis en automatización y análisis económico.