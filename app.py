#Caleb Schulz
#u0000020468
import requests
import pandas as pd
import streamlit as st

#API Integration and Caching
@st.cache_data
def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")
        return None

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd","per_page": 20}
data = fetch_data(url + "?" + "&".join(f"{k}={v}" for k, v in params.items()))

if data is None:
    st.stop()

df = pd.DataFrame(data)

#User Input Widgets
coins = st.multiselect("Select Coins", df["id"], default=[df["id"][0]])

days = st.slider("Select Days", 1, 30, 7)

#Dashboard Components
##KPI
row = df[df["id"] == coins[0]].iloc[0]
st.metric("Price", row["current_price"])

##Time Series Chart
for coin in coins:
    hist_url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    hist_params = {"vs_currency": "usd", "days": days}

    hist_data = fetch_data(hist_url + "?" + "&".join(f"{k}={v}" for k, v in hist_params.items()))

    if hist_data is None:
        continue

    prices = hist_data["prices"]
    hist_df = pd.DataFrame(prices, columns=["time", "price"])
    hist_df["time"] = pd.to_datetime(hist_df["time"], unit="ms")
    hist_df = hist_df.set_index("time")

    st.line_chart(hist_df["price"])

if not coins:
    st.warning("Please select a cryptocurrency first.")
    st.stop()

##Data Table
filtered = df[df["id"].isin(coins)]
st.dataframe(filtered[["id", "current_price", "market_cap"]])

# AI Usage: I used ChatGPT to help with debugging and understanding CoinGecko API. I made all the design decision.