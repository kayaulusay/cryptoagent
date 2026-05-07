import json
from openai import OpenAI

client = OpenAI(api_key = "")

def analyze_volume(volume_result: list[dict]):

    payload = {"current_result": volume_result}

    response = client.responses.create(
        model="gpt-5.2",
        reasoning={"effort": "medium"},
        input=[
            {
                "role": "system",
                "content": """
                    You are a crypto market analyst specializing in volume and liquidity signals.

                    You will receive a JSON array named "volume_results".
                    Each element has:
                    - coin (string): Binance trading symbol (e.g., "SOLUSDT", "BTCUSDT")
                    - current_volume (number): 24-hour quote volume from Binance `/api/v3/ticker/24hr`
                    - This value represents trading volume over the last 24 hours
                    - It is denominated in the quote asset (USDT for *USDT pairs*)

                    Your task:
                    1) Produce a relative volume interpretation across the provided coins ONLY (no external data).
                    2) Identify which coins show comparatively strong liquidity and trader attention versus the rest of this list.
                    3) Output a conservative, probabilistic signal that can be used as one feature in a short-term pump-likelihood model.
                    4) Do NOT guarantee returns or price direction.

                    Important constraints:
                    - Use ONLY relative comparisons within the provided input list.
                    - Do NOT assume what is “high” or “low” relative to the broader crypto market.
                    - Different coins naturally have different volume scales; normalize via ranking/percentiles.
                    - If any current_volume is missing, non-numeric, NaN, or <= 0, mark that coin as LOW confidence.

                    Return ONLY valid JSON (no markdown, no commentary) with EXACTLY this schema:

                    {
                    "results": [
                        {
                        "coin": string,
                        "current_volume": number,
                        "signal": {
                            "label": "HIGH_RELATIVE_VOLUME" | "MEDIUM_RELATIVE_VOLUME" | "LOW_RELATIVE_VOLUME",
                            "score": integer,        // 0–100, higher = stronger relative volume within this list
                            "confidence": integer   // 0–100, based on data validity and clarity of separation
                        },
                        "reasons": [string, string],
                        "watchouts": [string]
                        }
                    ],
                    "ranking": [string],
                    "summary": string
                    }

                    Scoring guidance:
                    - Rank coins by current_volume descending.
                    - Top ~25% → HIGH_RELATIVE_VOLUME
                    - Middle ~50% → MEDIUM_RELATIVE_VOLUME
                    - Bottom ~25% → LOW_RELATIVE_VOLUME
                    (If list size is small, approximate sensibly.)

                    Score bands:
                    - HIGH_RELATIVE_VOLUME: ~75–95
                    - MEDIUM_RELATIVE_VOLUME: ~45–74
                    - LOW_RELATIVE_VOLUME: ~10–44

                    Confidence guidance:
                    - Higher confidence when:
                    - current_volume values are valid and numeric
                    - separation between ranks is clear
                    - Lower confidence when:
                    - volumes are very close together
                    - data is missing, zero, or inconsistent

                    """

            },
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False)
                
            }
        ],

    )

    return json.loads(response.output_text)