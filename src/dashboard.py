import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np
import warnings
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Rutas relativas
data_path = os.path.join('src', 'static', 'data', 'enriched_historical.csv')

st.set_page_config(
    page_title="AVAL Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📊 AVAL Stock Analysis Dashboard (ARIMA)")

# Cargar datos enriquecidos
@st.cache_data
def load_data():
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("Filtros")
min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input(
    "Rango de fechas",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

show_sma21 = st.sidebar.checkbox("Mostrar SMA 21", value=True)
show_sma50 = st.sidebar.checkbox("Mostrar SMA 50", value=False)
show_bb = st.sidebar.checkbox("Mostrar Bandas de Bollinger", value=False)
show_rsi = st.sidebar.checkbox("Mostrar RSI", value=True)
show_momentum = st.sidebar.checkbox("Mostrar Momentum", value=False)
show_vol = st.sidebar.checkbox("Mostrar Volatilidad (7d)", value=False)
show_volume = st.sidebar.checkbox("Mostrar Volumen", value=False)

# --- MANEJO ROBUSTO DEL RANGO DE FECHAS ---
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, (pd.Timestamp, )):
    start_date = end_date = date_range
else:
    st.warning("Por favor selecciona un rango válido de fechas.")
    st.stop()

# Filtrar el dataframe
df_filtrado = df[
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
].copy()

if df_filtrado.empty:
    st.warning("No hay datos para el rango de fechas seleccionado. Por favor, elige un rango diferente.")
    st.stop()

# --- TABS ---
tabs = st.tabs(["📈 Gráfico de Precio", "📊 Indicadores", "🚦 Señales", "🧮 Métricas"])

# --- TAB 1: Gráfico de Precio ---
with tabs[0]:
    st.subheader("Precio y Medias Móviles")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df_filtrado['Date'],
        open=df_filtrado['Open AVAL'],
        high=df_filtrado['High AVAL'],
        low=df_filtrado['Low AVAL'],
        close=df_filtrado['Close AVAL'],
        name='OHLC'
    ))
    # SMA 21
    if show_sma21 and 'SMA_21' in df_filtrado:
        if len(df_filtrado.dropna(subset=['SMA_21'])) < 1 or len(df_filtrado) < 21:
            st.info("Selecciona al menos 21 días para ver la SMA 21.")
        else:
            fig.add_trace(go.Scatter(
                x=df_filtrado['Date'],
                y=df_filtrado['SMA_21'],
                name='SMA 21',
                line=dict(color='orange')
            ))
    # SMA 50
    if show_sma50 and 'SMA_50' in df_filtrado:
        if len(df_filtrado.dropna(subset=['SMA_50'])) < 1 or len(df_filtrado) < 50:
            st.info("Selecciona al menos 50 días para ver la SMA 50.")
        else:
            fig.add_trace(go.Scatter(
                x=df_filtrado['Date'],
                y=df_filtrado['SMA_50'],
                name='SMA 50',
                line=dict(color='green')
            ))
    # Bandas de Bollinger
    if show_bb and 'BB_upper' in df_filtrado and 'BB_lower' in df_filtrado:
        if len(df_filtrado.dropna(subset=['BB_upper', 'BB_lower'])) < 1 or len(df_filtrado) < 21:
            st.info("Selecciona al menos 21 días para ver las Bandas de Bollinger.")
        else:
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

# --- TAB 2: Indicadores ---
with tabs[1]:
    st.subheader("Indicadores Técnicos y KPIs")

    col1, col2, col3, col4, col5 = st.columns(5)

    def calc_change(series):
        if len(series) < 2:
            return None
        cambio = series.iloc[-1] - series.iloc[-2]
        cambio_pct = (cambio / series.iloc[-2]) * 100 if series.iloc[-2] != 0 else 0
        return cambio, cambio_pct

    # Obtener valores y cambios
    precio_actual = df_filtrado['Close AVAL'].dropna()
    precio_val = precio_actual.iloc[-1] if not precio_actual.empty else None
    precio_cambio = calc_change(precio_actual)

    vol_7d = df_filtrado['Volatility_7'].dropna() if 'Volatility_7' in df_filtrado else pd.Series(dtype=float)
    vol_val = vol_7d.iloc[-1] if not vol_7d.empty else None
    vol_cambio = calc_change(vol_7d)

    sma_21 = df_filtrado['SMA_21'].dropna() if 'SMA_21' in df_filtrado else pd.Series(dtype=float)
    sma_val = sma_21.iloc[-1] if not sma_21.empty else None
    sma_cambio = calc_change(sma_21)

    ret_acum = df_filtrado['Cumulative_Return'].dropna() if 'Cumulative_Return' in df_filtrado else pd.Series(dtype=float)
    ret_val = ret_acum.iloc[-1] if not ret_acum.empty else None
    ret_cambio = calc_change(ret_acum)

    rsi = df_filtrado['RSI'].dropna() if 'RSI' in df_filtrado else pd.Series(dtype=float)
    rsi_val = rsi.iloc[-1] if not rsi.empty else None
    rsi_cambio = calc_change(rsi)

    def format_arrow(val):
        if val is None:
            return ""
        return "▲" if val > 0 else ("▼" if val < 0 else "")

    def format_delta(val, is_percent=False):
        if val is None:
            return None
        return f"{val:.2f}%" if is_percent else f"{val:.4f}"

    # Precio Actual
    with col1:
        if precio_val is not None:
            st.metric(
                "Precio Actual",
                f"${precio_val:.2f}",
                delta=format_delta(precio_cambio[1], True)
            )
            st.markdown(f"<span style='font-size:20px;color:{'green' if precio_cambio and precio_cambio[0] > 0 else 'red' if precio_cambio and precio_cambio[0] < 0 else 'black'}'>{format_arrow(precio_cambio[0])}</span>", unsafe_allow_html=True)
        else:
            st.write("Precio Actual: N/A")
        with st.expander("¿Qué es el Precio Actual?"):
            st.write("El precio actual es el último precio de cierre registrado para la acción AVAL.")

    # Volatilidad 7d
    with col2:
        if vol_val is not None:
            st.metric(
                "Volatilidad (7d)",
                f"{vol_val:.4f}",
                delta=format_delta(vol_cambio[0])
            )
            st.markdown(f"<span style='font-size:20px;color:{'green' if vol_cambio and vol_cambio[0] > 0 else 'red' if vol_cambio and vol_cambio[0] < 0 else 'black'}'>{format_arrow(vol_cambio[0])}</span>", unsafe_allow_html=True)
        else:
            st.write("Volatilidad (7d): N/A")
        with st.expander("¿Qué es la Volatilidad?"):
            st.write("La volatilidad mide la desviación estándar móvil de 7 días del precio ajustado.")
            if vol_val is not None:
                if vol_val > 0.2:
                    st.warning("Alta volatilidad: el precio puede ser muy inestable.")
                elif vol_val < 0.05:
                    st.info("Baja volatilidad: el precio es relativamente estable.")
                else:
                    st.info("Volatilidad moderada.")

    # Media Móvil 21d
    with col3:
        if sma_val is not None:
            st.metric(
                "Media Móvil (21d)",
                f"${sma_val:.2f}",
                delta=format_delta(sma_cambio[0])
            )
            st.markdown(f"<span style='font-size:20px;color:{'green' if sma_cambio and sma_cambio[0] > 0 else 'red' if sma_cambio and sma_cambio[0] < 0 else 'black'}'>{format_arrow(sma_cambio[0])}</span>", unsafe_allow_html=True)
        else:
            st.write("Media Móvil (21d): N/A")
        with st.expander("¿Qué es la Media Móvil?"):
            st.write("La media móvil suaviza el precio para identificar tendencias a corto plazo.")

    # Retorno Acumulado
    with col4:
        if ret_val is not None:
            st.metric(
                "Retorno Acumulado",
                f"{ret_val:.2%}",
                delta=format_delta(ret_cambio[1], True)
            )
            st.markdown(f"<span style='font-size:20px;color:{'green' if ret_cambio and ret_cambio[0] > 0 else 'red' if ret_cambio and ret_cambio[0] < 0 else 'black'}'>{format_arrow(ret_cambio[0])}</span>", unsafe_allow_html=True)
        else:
            st.write("Retorno Acumulado: N/A")
        with st.expander("¿Qué es el Retorno Acumulado?"):
            st.write("El retorno acumulado es la ganancia o pérdida total desde el inicio del período.")
            if ret_val is not None:
                if ret_val > 0:
                    st.success("Retorno positivo: ganancia acumulada.")
                else:
                    st.error("Retorno negativo: pérdida acumulada.")

    # RSI
    with col5:
        if rsi_val is not None:
            st.metric(
                "RSI",
                f"{rsi_val:.2f}",
                delta=format_delta(rsi_cambio[1], True)
            )
            st.markdown(f"<span style='font-size:20px;color:{'green' if rsi_cambio and rsi_cambio[0] > 0 else 'red' if rsi_cambio and rsi_cambio[0] < 0 else 'black'}'>{format_arrow(rsi_cambio[0])}</span>", unsafe_allow_html=True)
        else:
            st.write("RSI: N/A")
        with st.expander("¿Qué es el RSI?"):
            st.write("El RSI mide la fuerza y velocidad de los movimientos de precio.")
            if rsi_val is not None:
                if rsi_val > 70:
                    st.warning("RSI alto: posible sobrecompra.")
                elif rsi_val < 30:
                    st.success("RSI bajo: posible sobreventa.")
                else:
                    st.info("RSI en zona neutral.")

    # Indicadores técnicos existentes (RSI, Momentum, Volatilidad, etc.)
    # RSI gráfico
    if show_rsi and 'RSI' in df_filtrado and len(df_filtrado) >= 14 and not df_filtrado['RSI'].dropna().empty:
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(
            x=df_filtrado['Date'],
            y=df_filtrado['RSI'],
            name='RSI',
            line=dict(color='purple')
        ))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
        fig_rsi.update_layout(template='plotly_dark', yaxis_title='RSI', height=200)
        st.plotly_chart(fig_rsi, use_container_width=True)
    # Momentum gráfico
    if show_momentum and 'Momentum' in df_filtrado and len(df_filtrado) >= 10 and not df_filtrado['Momentum'].dropna().empty:
        fig_mom = go.Figure()
        fig_mom.add_trace(go.Scatter(
            x=df_filtrado['Date'],
            y=df_filtrado['Momentum'],
            name='Momentum',
            line=dict(color='blue')
        ))
        fig_mom.update_layout(template='plotly_dark', yaxis_title='Momentum', height=200)
        st.plotly_chart(fig_mom, use_container_width=True)
    # Volatilidad gráfico
    if show_vol and 'Volatility_7' in df_filtrado and len(df_filtrado) >= 7 and not df_filtrado['Volatility_7'].dropna().empty:
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(
            x=df_filtrado['Date'],
            y=df_filtrado['Volatility_7'],
            name='Volatilidad 7d',
            line=dict(color='orange')
        ))
        fig_vol.update_layout(template='plotly_dark', yaxis_title='Volatilidad (7d)', height=200)
        st.plotly_chart(fig_vol, use_container_width=True)
    # Volumen gráfico
    if show_volume and 'Volume AVAL' in df_filtrado and not df_filtrado['Volume AVAL'].dropna().empty:
        fig_volu = go.Figure()
        fig_volu.add_trace(go.Bar(
            x=df_filtrado['Date'],
            y=df_filtrado['Volume AVAL'],
            name='Volumen'
        ))
        fig_volu.update_layout(template='plotly_dark', yaxis_title='Volumen', height=200)
        st.plotly_chart(fig_volu, use_container_width=True)

# --- TAB 3: Señales de Trading (solo resumen) ---
with tabs[2]:
    st.subheader("Resumen de Señales de Trading")
    # Cruce de medias móviles
    if show_sma21 and show_sma50 and 'SMA_21' in df_filtrado and 'SMA_50' in df_filtrado:
        if len(df_filtrado.dropna(subset=['SMA_21', 'SMA_50'])) < 51 or len(df_filtrado) < 51:
            st.info("Selecciona al menos 51 días para ver señales de cruce de medias móviles.")
        else:
            sma21 = df_filtrado['SMA_21']
            sma50 = df_filtrado['SMA_50']
            cruces = np.where(
                (sma21.shift(1) < sma50.shift(1)) & (sma21 > sma50), "Compra",
                np.where((sma21.shift(1) > sma50.shift(1)) & (sma21 < sma50), "Venta", None)
            )
            cruces_pos = np.where(~pd.isnull(cruces))[0]
            if len(cruces_pos) > 0:
                last_pos = cruces_pos[-1]
                st.info(f"Última señal de cruce de medias: {df_filtrado.iloc[last_pos]['Date'].date()} → **{cruces[last_pos]}**")
            else:
                st.write("No hay señales recientes de cruce de medias.")
    else:
        st.info("Activa ambas SMAs y selecciona al menos 51 días para ver señales de cruce de medias móviles.")

    # RSI sobrecompra/sobreventa
    if show_rsi and 'RSI' in df_filtrado and len(df_filtrado) >= 14 and not df_filtrado['RSI'].dropna().empty:
        rsi = df_filtrado['RSI']
        sobrecompra = rsi[rsi > 70]
        sobreventa = rsi[rsi < 30]
        if not sobrecompra.empty:
            st.warning(f"Última sobrecompra RSI: {df_filtrado.loc[sobrecompra.index[-1], 'Date'].date()} (RSI={sobrecompra.iloc[-1]:.2f})")
        if not sobreventa.empty:
            st.success(f"Última sobreventa RSI: {df_filtrado.loc[sobreventa.index[-1], 'Date'].date()} (RSI={sobreventa.iloc[-1]:.2f})")

    # Bandas de Bollinger
    if show_bb and 'BB_upper' in df_filtrado and 'BB_lower' in df_filtrado and len(df_filtrado) >= 21 and not df_filtrado['BB_upper'].dropna().empty and not df_filtrado['BB_lower'].dropna().empty:
        precio = df_filtrado['Adj Close AVAL']
        bb_upper = df_filtrado['BB_upper']
        bb_lower = df_filtrado['BB_lower']
        toques_sup = (precio >= bb_upper)
        toques_inf = (precio <= bb_lower)
        if toques_sup.any():
            idx = toques_sup[toques_sup].index[-1]
            st.warning(f"Último toque banda superior: {df_filtrado.loc[idx, 'Date'].date()}")
        if toques_inf.any():
            idx = toques_inf[toques_inf].index[-1]
            st.success(f"Último toque banda inferior: {df_filtrado.loc[idx, 'Date'].date()}")

# --- TAB 4: Métricas y Predicción ---
with tabs[3]:
    st.subheader("Predicción ARIMA y Métricas del Modelo (Dinámicas)")
    try:
        serie = df_filtrado.set_index('Date')['Adj Close AVAL'].dropna()
        if not isinstance(serie.index, pd.DatetimeIndex):
            serie.index = pd.to_datetime(serie.index)
        # Validación robusta del rango
        if len(serie) < 20:
            st.info("Selecciona un rango de fechas mayor (mínimo 20 datos) para realizar la predicción y calcular métricas ARIMA.")
        else:
            with st.spinner("Entrenando ARIMA con el rango seleccionado..."):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    arima_temp = ARIMA(serie, order=(3,1,1)).fit()
                # Predicción para el siguiente día hábil
                forecast = arima_temp.forecast(steps=1)
            last_date = serie.index[-1]
            next_date = last_date + pd.Timedelta(days=1)
            while next_date.weekday() >= 5:
                next_date += pd.Timedelta(days=1)
            st.success(f"Predicción para el {next_date.date()}: **${forecast.values[0]:.4f}**")

            # Métricas dinámicas (usando el ajuste in-sample)
            pred = arima_temp.predict(start=serie.index[1], end=serie.index[-1], typ='levels')
            y_true = serie[1:]
            y_pred = pred

            mae = mean_absolute_error(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            rmse = np.sqrt(mse)
            mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
            r2 = r2_score(y_true, y_pred)

            st.markdown("#### Métricas del Modelo ARIMA (para el rango seleccionado)")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("MAE", f"{mae:.4f}")
            with col2:
                st.metric("RMSE", f"{rmse:.4f}")
            with col3:
                st.metric("MAPE", f"{mape:.2f}%")
            with col4:
                st.metric("R²", f"{r2:.4f}")
    except Exception as e:
        st.info("No se pudo realizar la predicción ARIMA para el rango seleccionado.")
        st.exception(e)

    with st.expander("ℹ️ Información del Dataset"):
        st.write("Estadísticas Descriptivas:")
        stats_df = df_filtrado.drop(columns=['Date']).describe()
        st.dataframe(stats_df)
        st.write("Últimos Registros:")
        display_df = df_filtrado.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(display_df.tail())