# calcular_mercado.py
import yfinance as yf
import pandas as pd
from datetime import datetime

TICKERS = ["AAPL", "MSFT", "TSLA"]
PERIODO = "5y"

def calcular_datos(tickers, periodo):
    resultados = []
    for t in tickers:
        try:
            data = yf.download(t, period=periodo, interval="1mo", progress=False)
            if data.empty:
                continue
            maximo = data["High"].max()
            actual = data["Close"].iloc[-1]
            gap = float(((maximo - actual) / actual) * 100)

            resultados.append([t, float(maximo), float(actual), round(gap, 2)])
        except:
            continue
            
    return pd.DataFrame(resultados, columns=["ticker", "maximo", "actual", "gap"])

df = calcular_datos(TICKERS, PERIODO)
df["fecha"] = datetime.now().isoformat()

# Guardar el resultado en el repo
df.to_json("resultados.json", orient="records", indent=2)
