import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os

# Rutas relativas
DATA_PATH = os.path.join('src', 'static', 'data', 'enriched_historical.csv')
MODEL_PATH = os.path.join('src', 'static', 'models', 'arima_model.pkl')
METRICS_PATH = os.path.join('src', 'static', 'models', 'arima_metrics.csv')

st.set_page_config(
    page_title="AVAL Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📊 AVAL Stock Analysis Dashboard (ARIMA)")

# Cargar datos enriquecidos
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Cargar modelo ARIMA
try:
    arima_model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"Error al cargar el modelo ARIMA: {e}")
    st.stop()

# Cargar métricas
try:
    metrics = pd.read_csv(METRICS_PATH)
except Exception as e:
    st.error(f"Error al cargar las métricas: {e}")
    st.stop()

# ======================
# KPIs principales
# ======================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Precio Actual",
        f"${df['Adj Close AVAL'].iloc[-1]:.2f}",
        f"{df['Daily_Return'].iloc[-1]*100:.2f}%"
    )
    st.caption("Precio ajustado de cierre del último día.")

with col2:
    st.metric(
        "Volatilidad (7d)",
        f"{df['Volatility_7'].iloc[-1]:.4f}"
    )
    st.caption("Desviación estándar móvil de 7 días.")

with col3:
    st.metric(
        "Media Móvil (21d)",
        f"${df['SMA_21'].iloc[-1]:.2f}"
    )
    st.caption("Media móvil simple de 21 días.")

with col4:
    cumulative_return = (df['Cumulative_Return'].iloc[-1] - 1) * 100
    st.metric(
        "Retorno Acumulado",
        f"{cumulative_return:.2f}%"
    )
    st.caption("Retorno acumulado desde el inicio del periodo.")

with col5:
    st.metric(
        "Desviación Estándar Global",
        f"{df['Std_Adj_Close'].iloc[-1]:.4f}"
    )
    st.caption("Desviación estándar de toda la serie.")

# ======================
# Gráfico de precios y medias móviles
# ======================
st.subheader("Evolución del Precio y Medias Móviles")
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df['Date'],
    open=df['Open AVAL'],
    high=df['High AVAL'],
    low=df['Low AVAL'],
    close=df['Close AVAL'],
    name='OHLC'
))
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['SMA_21'],
    name='SMA 21',
    line=dict(color='orange')
))
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['SMA_50'],
    name='SMA 50',
    line=dict(color='green')
))
fig.update_layout(
    template='plotly_dark',
    xaxis_title='Fecha',
    yaxis_title='Precio',
    xaxis=dict(rangeslider=dict(visible=True), type="date")
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Predicción ARIMA
# ======================
st.subheader("Predicción ARIMA para el siguiente día")

# Predecir el siguiente día usando el modelo cargado
serie = df.set_index('Date')['Adj Close AVAL'].dropna()
from statsmodels.tsa.arima.model import ARIMAResults
import numpy as np

try:
    forecast = arima_model.forecast(steps=1)
    last_date = serie.index[-1]
    next_date = last_date + pd.Timedelta(days=1)

    # Ajustar para que sea el próximo día hábil
    if next_date.weekday() == 5:      # Sábado
        next_date += pd.Timedelta(days=2)
    elif next_date.weekday() == 6:    # Domingo
        next_date += pd.Timedelta(days=1)

    st.success(f"Predicción para el {next_date.date()}: **${forecast.values[0]:.4f}**")
except Exception as e:
    st.error(f"Error al predecir con ARIMA: {e}")

# Mostrar métricas del modelo
st.markdown("#### Métricas del Modelo ARIMA")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("MAE", f"{metrics['MAE'].iloc[0]:.4f}")
with col2:
    st.metric("RMSE", f"{metrics['RMSE'].iloc[0]:.4f}")
with col3:
    st.metric("MAPE", f"{metrics['MAPE'].iloc[0]:.2f}%")
with col4:
    st.metric("R²", f"{metrics['R2'].iloc[0]:.4f}")

# ======================
# Información adicional
# ======================
with st.expander("ℹ️ Información del Dataset"):
    st.write("Estadísticas Descriptivas:")
    stats_df = df.drop(columns=['Date']).describe()
    st.dataframe(stats_df)

    st.write("Últimos Registros:")
    display_df = df.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(display_df.tail())