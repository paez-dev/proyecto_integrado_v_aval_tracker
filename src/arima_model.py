import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import warnings

warnings.filterwarnings("ignore")

def cargar_datos_limpios(ruta_archivo='historical.csv'):
    """
    Carga el CSV, elimina filas de cabecera repetidas y asegura que el índice sea de fechas.
    """
    df = pd.read_csv(ruta_archivo)
    # Elimina filas donde 'Date' no es una fecha válida
    df = df[pd.to_datetime(df['Date'], errors='coerce').notna()]
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def obtener_serie(df, columna='Adj Close AVAL'):
    """
    Extrae la serie temporal de interés, asegurando que el índice es de fechas.
    """
    serie = df[columna].dropna()
    if not isinstance(serie.index, pd.DatetimeIndex):
        serie.index = pd.to_datetime(serie.index)
    return serie

def entrenar_arima(serie, order=(3,1,1)):
    model = ARIMA(serie, order=order)
    return model.fit()

def predecir_arima(fit, serie):
    pred = fit.predict(start=serie.index[1], end=serie.index[-1], typ='levels')
    pred.index = serie.index[1:]
    forecast = fit.forecast(steps=1)
    next_date = serie.index[-1] + pd.Timedelta(days=1)
    return pred, forecast, next_date

def calcular_metricas(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, mape, r2

def graficar_arima(serie, pred, forecast, next_date, order=(3,1,1)):
    plt.figure(figsize=(16,6))
    plt.plot(serie, label='Precio Real', color='blue')
    plt.plot(pred, label='Predicción ARIMA', color='orange', linestyle='--')
    plt.scatter(next_date, forecast.values[0], color='red', label=f'Predicción siguiente día ({next_date.date()})', zorder=5)
    plt.axvline(x=serie.index[-1], color='gray', linestyle=':', label='Último dato')
    plt.title(f'Precio Real vs Ajuste ARIMA{order} y Predicción del Siguiente Día')
    plt.xlabel('Fecha')
    plt.ylabel('Adj Close AVAL')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def guardar_modelo(modelo, ruta='src/static/models/arima_model.pkl'):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    joblib.dump(modelo, ruta)
    print(f"Modelo ARIMA guardado en {ruta}")

def guardar_metricas(mae, rmse, mape, r2, ruta='src/static/models/arima_metrics.csv'):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    metrics = pd.DataFrame([{
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'R2': r2
    }])
    metrics.to_csv(ruta, index=False)
    print(f"Métricas guardadas en {ruta}")

def ejecutar_arima_completo(
    ruta_archivo='src/static/data/historical.csv',
    columna='Adj Close AVAL',
    order=(3,1,1),
    graficar=True,
    guardar=True
):
    df = cargar_datos_limpios(ruta_archivo)
    serie = obtener_serie(df, columna)
    modelo = entrenar_arima(serie, order)
    pred, forecast, next_date = predecir_arima(modelo, serie)
    mae, rmse, mape, r2 = calcular_metricas(serie[1:], pred)
    if graficar:
        graficar_arima(serie, pred, forecast, next_date, order)
    print("📈 Métricas de Evaluación:")
    print(f"MAE  = {mae:.4f}")
    print(f"RMSE = {rmse:.4f}")
    print(f"MAPE = {mape:.2f}%")
    print(f"R²   = {r2:.4f}")
    print(f"\n📅 Predicción para el siguiente día ({next_date.date()}): {forecast.values[0]:.4f}")

    if guardar:
        modelo_path = 'src/static/models/arima_model.pkl'
        if os.path.exists(modelo_path):
            os.remove(modelo_path)
        guardar_modelo(modelo, modelo_path)
        guardar_metricas(mae, rmse, mape, r2, 'src/static/models/arima_metrics.csv')

    return {
        'serie': serie,
        'pred': pred,
        'forecast': forecast,
        'next_date': next_date,
        'modelo': modelo,
        'mae': mae,
        'rmse': rmse,
        'mape': mape,
        'r2': r2
    }

if __name__ == "__main__":
    ejecutar_arima_completo()