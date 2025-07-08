from fastapi import FastAPI
import requests
from utils import parse_flight_data

app = FastAPI()

API_KEY = "eccdb75d1e0924f0db51c9fb9be37256"  # Free AviationStack API key
BASE_URL = "http://api.aviationstack.com/v1/flights"


@app.get("/")
def index():
    return {"msg": "Airline Market Demand API is active."}


@app.get("/insights")
def fetch_flight_insights():
    payload = {"access_key": API_KEY, "limit": 50}

    try:
        resp = requests.get(BASE_URL, params=payload)
        flight_data = resp.json()
    except Exception as err:
        return {"error": "Failed to fetch flight data.", "details": str(err)}

    insights = parse_flight_data(flight_data)
    return insights
