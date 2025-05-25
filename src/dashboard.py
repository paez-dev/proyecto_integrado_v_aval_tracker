import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os
import numpy as np

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

# Filtros interactivos
st.sidebar.header("Filtros")
min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input("Rango de fechas", [min_date, max_date], min_value=min_date, max_value=max_date)
dias_semana = st.sidebar.multiselect("Día de la semana", options=df['Day_of_Week'].unique(), default=list(df['Day_of_Week'].unique()))
meses = st.sidebar.multiselect("Mes", options=sorted(df['Month'].unique()), default=sorted(df['Month'].unique()))
anios = st.sidebar.multiselect("Año", options=sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))

# Filtrar el dataframe
df_filtrado = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['Day_of_Week'].isin(dias_semana)) &
    (df['Month'].isin(meses)) &
    (df['Year'].isin(anios))
].copy()

# Selección de indicadores a mostrar
st.sidebar.header("Indicadores a mostrar")
show_sma21 = st.sidebar.checkbox("SMA 21", value=True)
show_sma50 = st.sidebar.checkbox("SMA 50", value=True)
show_bb = st.sidebar.checkbox("Bandas de Bollinger", value=True)
show_rsi = st.sidebar.checkbox("RSI", value=True)
show_momentum = st.sidebar.checkbox("Momentum", value=True)
show_vol = st.sidebar.checkbox("Volatilidad (7d)", value=True)
show_volume = st.sidebar.checkbox("Volumen", value=True)

# ======================
# Gráfico de precios y señales
# ======================
st.subheader("Evolución del Precio, Medias Móviles y Señales de Trading")
fig = go.Figure()

# OHLC
fig.add_trace(go.Candlestick(
    x=df_filtrado['Date'],
    open=df_filtrado['Open AVAL'],
    high=df_filtrado['High AVAL'],
    low=df_filtrado['Low AVAL'],
    close=df_filtrado['Close AVAL'],
    name='OHLC'
))

# Medias móviles
if show_sma21:
    fig.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['SMA_21'],
        name='SMA 21',
        line=dict(color='orange')
    ))
if show_sma50:
    fig.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['SMA_50'],
        name='SMA 50',
        line=dict(color='green')
    ))

# Bandas de Bollinger
if show_bb:
    fig.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['BB_upper'],
        name='Banda Superior',
        line=dict(color='lightblue', dash='dot')
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['BB_lower'],
        name='Banda Inferior',
        line=dict(color='lightblue', dash='dot')
    ))

fig.update_layout(
    template='plotly_dark',
    xaxis_title='Fecha',
    yaxis_title='Precio',
    xaxis=dict(rangeslider=dict(visible=True), type="date"),
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Señales de trading automáticas
# ======================
st.subheader("Señales de Trading Automáticas")

# Cruce de medias móviles
if show_sma21 and show_sma50:
    sma21 = df_filtrado['SMA_21']
    sma50 = df_filtrado['SMA_50']
    cruces = np.where((sma21.shift(1) < sma50.shift(1)) & (sma21 > sma50), "Compra",
                      np.where((sma21.shift(1) > sma50.shift(1)) & (sma21 < sma50), "Venta", None))
    cruces_idx = df_filtrado.index[~pd.isnull(cruces)]
    for idx in cruces_idx:
        st.info(f"Cruce de medias el {df_filtrado.loc[idx, 'Date'].date()}: Señal de **{cruces[idx]}**")

# RSI sobrecompra/sobreventa
if show_rsi:
    rsi = df_filtrado['RSI']
    for i, val in enumerate(rsi):
        if val > 70:
            st.warning(f"RSI sobrecompra el {df_filtrado.iloc[i]['Date'].date()} (RSI={val:.2f})")
        elif val < 30:
            st.success(f"RSI sobreventa el {df_filtrado.iloc[i]['Date'].date()} (RSI={val:.2f})")

# Toques de bandas de Bollinger
if show_bb:
    precio = df_filtrado['Adj Close AVAL']
    bb_upper = df_filtrado['BB_upper']
    bb_lower = df_filtrado['BB_lower']
    for i in range(len(precio)):
        if precio.iloc[i] >= bb_upper.iloc[i]:
            st.warning(f"El precio tocó la banda superior el {df_filtrado.iloc[i]['Date'].date()}")
        elif precio.iloc[i] <= bb_lower.iloc[i]:
            st.success(f"El precio tocó la banda inferior el {df_filtrado.iloc[i]['Date'].date()}")

# ======================
# Gráficos adicionales
# ======================
st.subheader("Indicadores Técnicos")

# RSI
if show_rsi:
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['RSI'],
        name='RSI',
        line=dict(color='purple')
    ))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
    fig_rsi.update_layout(template='plotly_dark', yaxis_title='RSI', height=250)
    st.plotly_chart(fig_rsi, use_container_width=True)

# Momentum
if show_momentum:
    fig_mom = go.Figure()
    fig_mom.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['Momentum'],
        name='Momentum',
        line=dict(color='blue')
    ))
    fig_mom.update_layout(template='plotly_dark', yaxis_title='Momentum', height=250)
    st.plotly_chart(fig_mom, use_container_width=True)

# Volatilidad
if show_vol:
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(
        x=df_filtrado['Date'],
        y=df_filtrado['Volatility_7'],
        name='Volatilidad 7d',
        line=dict(color='orange')
    ))
    fig_vol.update_layout(template='plotly_dark', yaxis_title='Volatilidad (7d)', height=250)
    st.plotly_chart(fig_vol, use_container_width=True)

# Volumen
if show_volume:
    fig_volu = go.Figure()
    fig_volu.add_trace(go.Bar(
        x=df_filtrado['Date'],
        y=df_filtrado['Volume_AVAL'],
        name='Volumen'
    ))
    fig_volu.update_layout(template='plotly_dark', yaxis_title='Volumen', height=250)
    st.plotly_chart(fig_volu, use_container_width=True)

# ======================
# KPIs principales con explicación e interpretación
# ======================
st.subheader("KPIs Principales")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    precio_actual = df_filtrado['Adj Close AVAL'].iloc[-1]
    daily_return = df_filtrado['Daily_Return'].iloc[-1]
    st.metric("Precio Actual", f"${precio_actual:.2f}", f"{daily_return*100:.2f}%")
    with st.expander("¿Qué es?"):
        st.write("Precio ajustado de cierre del último día.")
    if daily_return > 0.01:
        st.success("El precio subió significativamente hoy.")
    elif daily_return < -0.01:
        st.error("El precio cayó significativamente hoy.")
    else:
        st.info("El precio tuvo pocos cambios hoy.")

with col2:
    vol_7d = df_filtrado['Volatility_7'].iloc[-1]
    st.metric("Volatilidad (7d)", f"{vol_7d:.4f}")
    with st.expander("¿Qué es?"):
        st.write("Desviación estándar móvil de 7 días.")
    if vol_7d > 0.2:
        st.warning("Alta volatilidad: el precio está variando mucho.")
    elif vol_7d < 0.05:
        st.info("Baja volatilidad: el precio es estable.")
    else:
        st.info("Volatilidad moderada.")

with col3:
    sma_21 = df_filtrado['SMA_21'].iloc[-1]
    precio = df_filtrado['Adj Close AVAL'].iloc[-1]
    st.metric("Media Móvil (21d)", f"${sma_21:.2f}")
    with st.expander("¿Qué es?"):
        st.write("Media móvil simple de 21 días.")
    if precio > sma_21:
        st.success("El precio está por encima de la media móvil: tendencia alcista.")
    elif precio < sma_21:
        st.error("El precio está por debajo de la media móvil: tendencia bajista.")
    else:
        st.info("El precio está igual a la media móvil.")

with col4:
    cumulative_return = (df_filtrado['Cumulative_Return'].iloc[-1] - 1) * 100
    st.metric("Retorno Acumulado", f"{cumulative_return:.2f}%")
    with st.expander("¿Qué es?"):
        st.write("Retorno acumulado desde el inicio del periodo.")
    if cumulative_return > 0:
        st.success("Rentabilidad positiva en el periodo.")
    else:
        st.error("Rentabilidad negativa en el periodo.")

with col5:
    std_global = df_filtrado['Std_Adj_Close'].iloc[-1]
    st.metric("Desviación Estándar Global", f"{std_global:.4f}")
    with st.expander("¿Qué es?"):
        st.write("Desviación estándar de toda la serie.")
    if std_global > 0.2:
        st.warning("Alta dispersión histórica de precios.")
    elif std_global < 0.05:
        st.info("Poca dispersión histórica de precios.")
    else:
        st.info("Dispersión moderada.")

# ======================
# Predicción ARIMA
# ======================
st.subheader("Predicción ARIMA para el siguiente día")
try:
    arima_model = joblib.load(MODEL_PATH)
    serie = df_filtrado.set_index('Date')['Adj Close AVAL'].dropna()
    forecast = arima_model.forecast(steps=1)
    last_date = serie.index[-1]
    next_date = last_date + pd.Timedelta(days=1)
    if next_date.weekday() == 5:
        next_date += pd.Timedelta(days=2)
    elif next_date.weekday() == 6:
        next_date += pd.Timedelta(days=1)
    st.success(f"Predicción para el {next_date.date()}: **${forecast.values[0]:.4f}**")
except Exception as e:
    st.error(f"Error al predecir con ARIMA: {e}")

# Mostrar métricas del modelo
try:
    metrics = pd.read_csv(METRICS_PATH)
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
except Exception as e:
    st.error(f"Error al cargar las métricas: {e}")

# ======================
# Información adicional
# ======================
with st.expander("ℹ️ Información del Dataset"):
    st.write("Estadísticas Descriptivas:")
    stats_df = df_filtrado.drop(columns=['Date']).describe()
    st.dataframe(stats_df)
    st.write("Últimos Registros:")
    display_df = df_filtrado.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(display_df.tail())