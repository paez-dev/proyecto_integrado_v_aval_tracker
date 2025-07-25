import csv
import os
from datetime import datetime

def init_csv_log(file_path="src/logs/log_data.csv"):
    """Inicializa el archivo CSV si no existe y agrega los encabezados."""
    # Verificar si el directorio existe, si no, crear
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    # Verificar si el archivo CSV existe, si no, crear con encabezado
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Fecha", "Símbolo", "Registros_descargados", "Registros_agregados", "Total_en_archivo", "Estado"])
            writer.writeheader()

def write_csv_log(symbol, downloaded_count, new_rows_added, total_count, status):
    """Escribe un nuevo registro en el archivo CSV de log."""
    log_entry = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Símbolo": symbol,
        "Registros_descargados": downloaded_count,
        "Registros_agregados": new_rows_added,
        "Total_en_archivo": total_count,
        "Estado": status
    }

    log_data_path = "src/logs/log_data.csv"

    # Verificar si el directorio existe, si no, crear
    dir_path = os.path.dirname(log_data_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    # Solo se escribe el encabezado la primera vez, cuando el archivo no existe
    file_exists = os.path.exists(log_data_path)

    with open(log_data_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Fecha", "Símbolo", "Registros_descargados", "Registros_agregados", "Total_en_archivo", "Estado"])
        
        # Si el archivo no existe, se escribe el encabezado
        if not file_exists:
            writer.writeheader()
        
        # Escribir la nueva entrada
        writer.writerow(log_entry)