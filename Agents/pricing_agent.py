import json
from openai import OpenAI

client = OpenAI(api_key = "")

def analyze_pricing(current_price_data: list[dict], price_history_data: list[dict]):

    payload = {
        "current_price_data": current_price_data,
        "price_history_data": price_history_data,
        "timepoints_days": [7, 30, 90, 365]
    }

    response = client.responses.create(
        model="gpt-5.2",
        reasoning={"effort": "medium"},
        input=[
            {
                "role": "system",
                "content": """
                        You are a crypto price-structure analyst.

                        You will receive two JSON arrays:
                        1) current_price_data: list of objects with keys:
                        - "Coin Name" (symbol)
                        - "Current Price" (string or number)
                        2) price_history_data: list of objects with keys:
                        - "Coin Name" (symbol)
                        - "prices" (object) containing some/all of:
                            "price before 7 days", "price before 30 days", "price before 90 days", "price before 365 days"

                        Goal:
                        - For each symbol, infer basic trend and whether price looks extended or has room.
                        - Use only the provided prices. Do not use external data.
                        - Use probabilistic language. Do NOT guarantee returns.

                        Compute (per symbol) where possible:
                        - r7   = (current - p7)   / p7
                        - r30  = (current - p30)  / p30
                        - r90  = (current - p90)  / p90
                        - r365 = (current - p365) / p365
                        If a timepoint is missing/invalid (0/null), output null for that return.

                        Interpretation guidance:
                        - If returns are positive across multiple horizons: UPTREND.
                        - If returns are negative across multiple horizons: DOWNTREND.
                        - Mixed: RANGE or MIXED.
                        - EXTENDED if short-horizon return is very large positive AND longer-horizon returns are also strongly positive.
                        - DEPRESSED if short-horizon return is very negative AND longer-horizon returns are also negative/weak.
                        - NORMAL otherwise.
                        - If too much data is missing, use UNKNOWN and lower confidence.

                        Return ONLY valid JSON (no markdown, no commentary) with EXACTLY this schema:

                        {
                        "results": [
                            {
                            "symbol": string,
                            "prices": {
                                "current": number,
                                "p7": number | null,
                                "p30": number | null,
                                "p90": number | null,
                                "p365": number | null
                            },
                            "returns": {
                                "r7": number | null,
                                "r30": number | null,
                                "r90": number | null,
                                "r365": number | null
                            },
                            "signal": {
                                "trend_label": "UPTREND" | "DOWNTREND" | "RANGE" | "MIXED",
                                "extension_label": "EXTENDED" | "NORMAL" | "DEPRESSED" | "UNKNOWN",
                                "trend_score": integer,
                                "room_score": integer,
                                "confidence": integer
                            },
                            "reasons": [string, string],
                            "watchouts": [string]
                            }
                        ],
                        "ranking_by_room": [string],
                        "ranking_by_trend": [string],
                        "summary": string
                        }

                        Scoring guidance (0-100):
                        - trend_score: higher when multiple available returns align positive; lower when they align negative.
                        - room_score: higher when NOT EXTENDED and there is plausible room for continuation/recovery.
                        - confidence: higher when more timepoints exist and returns are consistent; lower when missing/mixed.
                        """
            },
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False)
                
            }
        ],

    )

    return json.loads(response.output_text)
