import requests
import json
import time

coin_id = "thorchain"
vs = "usd"
url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
params = {"vs_currency": vs, "days": 30, "interval": "daily"}

print(f"🔍 Teste CoinGecko-Chart für {coin_id} ...")
resp = requests.get(url, params=params, timeout=20)

print(f"HTTP-Status: {resp.status_code}")

if resp.status_code == 429:
    print("⚠️ Rate Limit erreicht (429) – CoinGecko blockt aktuell zu viele Requests.")
    exit(1)

data = resp.json()
prices = data.get("prices", [])
print(f"Anzahl Preis-Punkte: {len(prices)}")

if len(prices) > 0:
    first_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(prices[0][0] / 1000))
    last_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(prices[-1][0] / 1000))
    print(f"Zeitraum: {first_date} → {last_date}")
else:
    print("❌ Keine Preisdaten empfangen – API antwortet leer oder gesperrt.")

