"""
Core advisory agent — generates sell/hold recommendations in Tamil.
Uses price data from price_fetcher and OpenAI for natural language advice.
"""

import os
import requests
from dotenv import load_dotenv
from src.price_fetcher import fetch_prices, get_all_market_prices

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

SYSTEM_PROMPT = """நீங்கள் ஒரு விவசாய ஆலோசகர். தமிழ்நாட்டு விவசாயிகளுக்கு சந்தை விலை தகவல்களை வைத்து 
விற்கலாமா அல்லது காத்திருக்கலாமா என்று எளிய தமிழில் ஆலோசனை கூறுங்கள்.
பதில் குறுகியதாகவும் தெளிவாகவும் இருக்க வேண்டும். அதிகபட்சம் 3 வரிகள்."""


def get_advisory(commodity: str, market: str = None) -> dict:
    """
    Fetch prices for a commodity and return Tamil sell/hold advisory.
    Returns: {commodity, prices, advice_tamil, action}
    """
    prices = fetch_prices(commodity=commodity, market=market)

    if not prices:
        return {
            "commodity": commodity,
            "prices": [],
            "advice_tamil": "இன்று இந்த பொருளுக்கு விலை தகவல் கிடைக்கவில்லை. நாளை மீண்டும் முயற்சிக்கவும்.",
            "action": "wait",
        }

    latest = prices[0]
    modal = latest["modal_price"]
    min_p = latest["min_price"]
    max_p = latest["max_price"]

    price_summary = (
        f"பொருள்: {commodity}\n"
        f"சந்தை: {latest['market']}, {latest['district']}\n"
        f"தேதி: {latest['date']}\n"
        f"குறைந்தபட்ச விலை: ₹{min_p}/குவிண்டால்\n"
        f"அதிகபட்ச விலை: ₹{max_p}/குவிண்டால்\n"
        f"சராசரி விலை: ₹{modal}/குவிண்டால்\n"
    )

    user_message = (
        f"{price_summary}\n"
        f"இந்த விலையில் விவசாயி இப்போது விற்கலாமா அல்லது காத்திருக்கலாமா? "
        f"விற்க வேண்டும் என்றால் 'விற்கவும்', காத்திருக்க வேண்டும் என்றால் 'காத்திருக்கவும்' என்று தெளிவாக சொல்லுங்கள்."
    )

    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": SYSTEM_PROMPT + "\n\n" + user_message,
        "stream": False,
    }, timeout=60)
    response.raise_for_status()
    advice = response.json()["response"].strip()
    action = "sell" if "விற்கவும்" in advice else "hold"

    return {
        "commodity": commodity,
        "prices": prices,
        "advice_tamil": advice,
        "action": action,
        "modal_price": modal,
    }


def get_market_summary(district: str = None) -> list[dict]:
    """Get advisory for all commodities available in the district today."""
    all_prices = get_all_market_prices(district=district)
    if not all_prices:
        return []

    # Group by commodity, take first record per commodity
    seen = {}
    for p in all_prices:
        if p["commodity"] not in seen:
            seen[p["commodity"]] = p

    summaries = []
    for commodity, price in seen.items():
        summaries.append({
            "commodity": commodity,
            "modal_price": price["modal_price"],
            "min_price": price["min_price"],
            "max_price": price["max_price"],
            "market": price["market"],
            "date": price["date"],
        })
    return summaries
