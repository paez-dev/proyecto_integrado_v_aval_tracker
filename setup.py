from setuptools import setup, find_packages

setup(
    name="proyecto_integrado_v_aval_tracker",
    version="0.0.2",
    author="Jean Carlos Páez Ramírez",
    author_email="",
    description="Paquete para descargas de datos del grupo AVAL de Yahoo Finance",
    py_modules=["actividad_2"],
    packages=find_packages(),  # Detecta automáticamente los paquetes
    install_requires=[
        "pandas>=2.2.3",  # Necesario para manipulación de datos
        'numpy',
        'scikit-learn',
        'streamlit',
        'plotly',
        'matplotlib',
        "joblib",
        "yfinance>=0.1.64",  # Necesario para descargar datos de Yahoo Finance
        "statsmodels",
    ],
    python_requires=">=3.6",  # Indica la versión mínima de Python
)