"""
Tamil output formatter — formats price and advisory data into Tamil messages
suitable for WhatsApp, SMS, or voice (TTS-ready text).
"""

from datetime import date


def format_price_message(commodity: str, modal_price: float, min_price: float,
                          max_price: float, market: str, advice: str) -> str:
    """Returns a Tamil WhatsApp/SMS-ready message."""
    today = date.today().strftime("%d/%m/%Y")
    action_line = "✅ இப்போது விற்கவும்" if "விற்கவும்" in advice else "⏳ இன்னும் காத்திருக்கவும்"

    return (
        f"🌾 *விவசாய விலை அறிவிப்பு* 🌾\n"
        f"தேதி: {today}\n"
        f"சந்தை: {market}\n\n"
        f"பொருள்: *{commodity}*\n"
        f"குறைந்த விலை: ₹{min_price:.0f}\n"
        f"அதிக விலை:   ₹{max_price:.0f}\n"
        f"சராசரி விலை: ₹{modal_price:.0f} /குவிண்டால்\n\n"
        f"ஆலோசனை:\n{advice}\n\n"
        f"{action_line}"
    )


def format_voice_script(commodity: str, modal_price: float, advice: str) -> str:
    """Returns plain Tamil text suitable for Text-to-Speech (IVR calls)."""
    return (
        f"வணக்கம். இன்றைய {commodity} விலை குவிண்டாலுக்கு "
        f"சராசரியாக {modal_price:.0f} ரூபாய். "
        f"{advice}"
    )


def format_no_data_message(commodity: str) -> str:
    return (
        f"🌾 {commodity} பொருளுக்கு இன்று விலை தகவல் கிடைக்கவில்லை.\n"
        f"நாளை மீண்டும் முயற்சிக்கவும்."
    )
