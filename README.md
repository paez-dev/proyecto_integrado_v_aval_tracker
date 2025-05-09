---

## Proyecto Integrado V - Grupo Aval Tracker (AVAL)

Este proyecto tiene como objetivo automatizar la recolección continua de datos históricos del **Grupo Aval (AVAL)**, 
una de las principales entidades financieras de Colombia. Los datos se obtienen desde **Yahoo Finanzas**, se almacenan 
en formato `.csv` y se actualizan automáticamente mediante **GitHub Actions**, manteniendo la trazabilidad y 
persistencia del histórico.

---

## 📌 Características

* 🔄 **Automatización diaria con GitHub Actions**: Los datos se actualizan automáticamente cada día a las 12:00 UTC.
* 📊 **Almacenamiento histórico en `CSV`**: Los datos se mantienen en formato CSV para facilitar su análisis.
* 🔍 **Logs de ejecución para trazabilidad**: Se guarda un archivo `log_data.csv` con los registros de cada ejecución.
* 🧱 **Implementación con Programación Orientada a Objetos (OOP)**: El código se organiza utilizando principios de OOP.
* 🧪 **Recolector de datos con `yfinance` y `pandas`**: El colector de datos descarga los datos históricos de Yahoo Finanzas y los guarda en un archivo CSV.

---

## ⚙️ Tecnologías utilizadas

* Python 3.10
* [yfinance](https://pypi.org/project/yfinance/)
* pandas
* logging
* GitHub Actions

---

## 📈 Indicador económico

* **Activo**: Grupo Aval Acciones y Valores S.A.
* **Símbolo**: `AVAL`
* [🔗 Ver en Yahoo Finanzas](https://es-us.finanzas.yahoo.com/quote/AVAL/)

---

## 📁 Estructura del repositorio

```
proyecto_integrado_v_aval/
├── .github/
│   └── workflows/
│       └── update_data.yml      # Flujo automático de actualización con GitHub Actions
│
├── docs/
│   └── report_entrega1.pdf      # Informe académico en formato APA
│
├── src/
│   ├── collector.py             # Descarga y persistencia de datos
│   ├── logger.py                # Configuración de logs
│   └── static/
│       └── historical.csv       # Datos históricos de AVAL
│
├── log_data.csv                # Archivo que guarda los logs de cada ejecución
├── README.md
└── .gitignore
```

---

## 🚀 Instrucciones de uso

1. **Instala dependencias**:

   ```bash
   pip install yfinance pandas
   ```

2. **Ejecuta el colector localmente**:
   Si deseas ejecutar el colector de datos manualmente en tu máquina local, utiliza el siguiente comando:

   ```bash
   python src/collector.py
   ```

3. **Automatización con GitHub Actions**:
   Si prefieres que el proceso sea completamente automático, puedes configurar **GitHub Actions** para que se ejecute diariamente. 
   El flujo de trabajo configurado en `update_data.yml` se encargará de actualizar los datos todos los días a las 12:00 UTC.

   * El flujo de trabajo de GitHub Actions descargará los datos de Yahoo Finanzas, los almacenará en el archivo `historical.csv` y realizará un commit y push automático al repositorio con los nuevos datos.
   * **Logs de ejecución**: Cada vez que se ejecute el flujo de trabajo, se guardarán registros detallados en el archivo `log_data.csv` para monitorear el éxito o fracaso de cada ejecución.
   * Puedes ver los logs de ejecución en la interfaz de GitHub Actions para verificar el resultado de cada ejecución.

---

## 📄 Licencia

Este proyecto es de uso educativo y forma parte de la asignatura **Proyecto Integrado V**, bajo la línea de énfasis en automatización y análisis económico.

---

### Explicación de la estructura del repositorio:

* **`.github/workflows/update_data.yml`**: Contiene el archivo del flujo de trabajo de **GitHub Actions** que ejecuta automáticamente el proceso de recolección y actualización de los datos de `AVAL`.

* **`src/collector.py`**: Este es el script principal para descargar los datos históricos de Yahoo Finanzas y almacenarlos en un archivo CSV llamado `historical.csv`.

* **`src/logger.py`**: Archivo que contiene la configuración del sistema de logs, registrando cada ejecución del flujo de trabajo para trazabilidad.

* **`src/static/historical.csv`**: Este archivo almacena los datos históricos de **Grupo Aval**. Este archivo se actualizará automáticamente con cada ejecución programada.

* **`log_data.csv`**: Este archivo en la raíz del repositorio guarda los logs de cada ejecución, detallando el éxito o fracaso del proceso de actualización, lo que facilita el monitoreo.

* **`README.md`**: Este archivo contiene la documentación y las instrucciones de uso del proyecto.

* **`.gitignore`**: Archivo que excluye archivos y directorios innecesarios del repositorio, como dependencias de Python o archivos temporales.

---
