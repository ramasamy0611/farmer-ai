# FarmerAI 🌾

Agri loss prevention agent for Tamil Nadu farmers (Oddanchatram / Dindigul).

Fetches daily market prices from Agmarknet and gives Tamil sell/hold advisory via WhatsApp, SMS, or voice call.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys
```

Get free API keys:
- data.gov.in key: https://data.gov.in/user/register
- OpenAI key: https://platform.openai.com/api-keys

## Run

```bash
# All commodities in Dindigul today
python main.py

# Advisory for a specific commodity
python main.py Tomato
python main.py Onion
```

## Sample Output (Tamil)

```
🌾 விவசாய விலை அறிவிப்பு 🌾
தேதி: 23/05/2026
சந்தை: Oddanchatram

பொருள்: Tomato
குறைந்த விலை: ₹800
அதிக விலை:   ₹1200
சராசரி விலை: ₹1000 /குவிண்டால்

ஆலோசனை:
விலை நல்லபடியாக உள்ளது. இப்போதே விற்கவும்.

✅ இப்போது விற்கவும்
```

## Project Structure

```
farmer-ai/
├── src/
│   ├── price_fetcher.py   # Agmarknet API integration
│   ├── advisor.py         # OpenAI advisory agent
│   └── tamil_output.py    # Tamil message formatter
├── main.py                # Entry point
├── requirements.txt
└── .env.example
```
