import pandas as pd
import numpy as np
from datetime import datetime
import os

class DataEnricher:
    def __init__(self, input_file):
        self.input_path = os.path.join('src', 'static', 'data', input_file)
        self.df = pd.read_csv(self.input_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])

    def add_temporal_features(self):
        self.df['Day_of_Week'] = self.df['Date'].dt.day_name()
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Quarter'] = self.df['Date'].dt.quarter

    def add_technical_indicators(self):
        # Medias móviles
        self.df['SMA_7'] = self.df['Adj Close AVAL'].rolling(window=7).mean()
        self.df['SMA_21'] = self.df['Adj Close AVAL'].rolling(window=21).mean()
        self.df['SMA_50'] = self.df['Adj Close AVAL'].rolling(window=50).mean()
        self.df['SMA_100'] = self.df['Adj Close AVAL'].rolling(window=100).mean()
        self.df['SMA_200'] = self.df['Adj Close AVAL'].rolling(window=200).mean()

        # Volatilidad (desviación estándar móvil)
        self.df['Volatility_7'] = self.df['Adj Close AVAL'].rolling(window=7).std()
        self.df['Volatility_14'] = self.df['Adj Close AVAL'].rolling(window=14).std()
        self.df['Volatility_30'] = self.df['Adj Close AVAL'].rolling(window=30).std()

        # Desviación estándar global
        self.df['Std_Adj_Close'] = self.df['Adj Close AVAL'].expanding().std()

        # Retornos diarios del precio ajustado
        self.df['Daily_Return'] = self.df['Adj Close AVAL'].pct_change()

        # Retorno total diario incluyendo dividendos en fechas específicas
        self.df['Total_Daily_Return'] = self.df['Daily_Return'].fillna(0)
        dividend_days = self.df['Dividends AVAL'] > 0
        self.df.loc[dividend_days, 'Total_Daily_Return'] += self.df['Dividends AVAL'] / self.df['Adj Close AVAL'].shift(1)

        # Retorno acumulado total con dividendos
        self.df['Total_Cumulative_Return'] = (1 + self.df['Total_Daily_Return']).cumprod()

        # Retorno acumulado solo con precio (como antes)
        self.df['Cumulative_Return'] = (1 + self.df['Daily_Return']).cumprod()

        # Tasa de variación absoluta y porcentual
        self.df['Price_Change'] = self.df['Adj Close AVAL'].diff()
        self.df['Price_Change_Pct'] = self.df['Adj Close AVAL'].pct_change() * 100

        # RSI
        delta = self.df['Adj Close AVAL'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.df['RSI'] = 100 - (100 / (1 + rs))

        # Momentum
        self.df['Momentum'] = self.df['Adj Close AVAL'].diff(periods=7)

        # Bandas de Bollinger
        self.df['BB_middle'] = self.df['Adj Close AVAL'].rolling(window=20).mean()
        std_dev = self.df['Adj Close AVAL'].rolling(window=20).std()
        self.df['BB_upper'] = self.df['BB_middle'] + (std_dev * 2)
        self.df['BB_lower'] = self.df['BB_middle'] - (std_dev * 2)

        # Media móvil de volumen
        self.df['Volume_MA_21'] = self.df['Volume AVAL'].rolling(window=21).mean()

    def enrich_data(self, output_file):
        self.add_temporal_features()
        self.add_technical_indicators()

        # Crear el directorio si no existe
        output_dir = os.path.join('src', 'static', 'data')
        os.makedirs(output_dir, exist_ok=True)

        # Guarda los datos enriquecidos
        output_path = os.path.join(output_dir, output_file)
        self.df.to_csv(output_path, index=False)
        return self.df

def main():
    try:
        enricher = DataEnricher('historical.csv')
        enriched_df = enricher.enrich_data('enriched_historical.csv')

        print("\nColumnas en el dataset enriquecido:")
        print(enriched_df.columns.tolist())
        print("\nPrimeras filas del dataset enriquecido:")
        print(enriched_df.head())

        print("\nEstadísticas de los nuevos indicadores:")
        new_indicators = [
            'SMA_7', 'SMA_21', 'SMA_50', 'SMA_100', 'SMA_200',
            'Volatility_7', 'Volatility_14', 'Volatility_30',
            'Std_Adj_Close', 'Daily_Return', 'Cumulative_Return',
            'Price_Change', 'Price_Change_Pct', 'RSI', 'Momentum',
            'BB_middle', 'BB_upper', 'BB_lower', 'Volume_MA_21'
        ]
        print(enriched_df[new_indicators].describe())

        print("\nProceso de enriquecimiento completado exitosamente.")

    except Exception as e:
        print(f"\nError durante el proceso de enriquecimiento: {e}")

if __name__ == "__main__":
    main()