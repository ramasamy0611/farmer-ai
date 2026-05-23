"""
Market price fetcher using data.gov.in Agmarknet API.
Fetches daily commodity prices for Oddanchatram / Dindigul, Tamil Nadu.
"""

import os
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DATA_GOV_API_KEY")
BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

DEFAULT_STATE = os.getenv("DEFAULT_STATE", "Tamil Nadu")
DEFAULT_DISTRICT = os.getenv("DEFAULT_DISTRICT", "Dindigul")
DEFAULT_MARKET = os.getenv("DEFAULT_MARKET", "Oddanchatram")


def fetch_prices(commodity: str = None, market: str = None, district: str = None) -> list[dict]:
    """
    Fetch today's commodity prices from Agmarknet via data.gov.in.
    Returns list of price records: [{commodity, market, min_price, max_price, modal_price, date}]
    """
    market = market or DEFAULT_MARKET
    district = district or DEFAULT_DISTRICT

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 50,
        "filters[State]": DEFAULT_STATE,
        "filters[District]": district,
        "filters[Market]": market,
    }
    if commodity:
        params["filters[Commodity]"] = commodity

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", [])
        return [_normalize(r) for r in records]
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch prices: {e}")
        return []


def _normalize(record: dict) -> dict:
    return {
        "commodity": record.get("Commodity", ""),
        "variety": record.get("Variety", ""),
        "market": record.get("Market", ""),
        "district": record.get("District", ""),
        "min_price": float(record.get("Min Price", 0)),
        "max_price": float(record.get("Max Price", 0)),
        "modal_price": float(record.get("Modal Price", 0)),
        "date": record.get("Arrival Date", str(date.today())),
        "unit": "Rs/Quintal",
    }


def get_all_market_prices(district: str = None) -> list[dict]:
    """Fetch all commodity prices for the district (not filtered by market)."""
    district = district or DEFAULT_DISTRICT
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 100,
        "filters[State]": DEFAULT_STATE,
        "filters[District]": district,
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return [_normalize(r) for r in response.json().get("records", [])]
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return []
