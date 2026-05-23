"""
FarmerAI — Agri Loss Prevention Agent
Usage: python main.py [commodity]
Example: python main.py Tomato
"""

import sys
from src.advisor import get_advisory, get_market_summary
from src.tamil_output import format_price_message, format_voice_script, format_no_data_message


def run(commodity: str = None):
    if commodity:
        print(f"\nFetching advisory for: {commodity}\n")
        result = get_advisory(commodity)

        if not result["prices"]:
            print(format_no_data_message(commodity))
            return

        msg = format_price_message(
            commodity=result["commodity"],
            modal_price=result["modal_price"],
            min_price=result["prices"][0]["min_price"],
            max_price=result["prices"][0]["max_price"],
            market=result["prices"][0]["market"],
            advice=result["advice_tamil"],
        )
        print(msg)
        print("\n--- Voice Script (TTS) ---")
        print(format_voice_script(commodity, result["modal_price"], result["advice_tamil"]))

    else:
        print("\nFetching all commodity prices for Dindigul district...\n")
        summaries = get_market_summary()
        if not summaries:
            print("No data available today.")
            return
        for s in summaries:
            print(f"{s['commodity']:20} ₹{s['modal_price']:>8.0f}/qtl  [{s['market']}]")


if __name__ == "__main__":
    commodity = sys.argv[1] if len(sys.argv) > 1 else None
    run(commodity)
