import json
from openai import OpenAI

client = OpenAI(api_key = "")

def analyze_btc_dom (btc_dominance: float):

    response = client.responses.create(
        model = "gpt-5.2",
        reasoning = {"effort": "medium"},
        input = [
            {
                "role": "system",
                "content": f"""
                        You are a crypto market regime analyst.

                        BTC dominance is {btc_dominance:.2f}%.

                        Return ONLY valid JSON with:
                        - regime_label: ALT_FRIENDLY | BTC_FRIENDLY | NEUTRAL
                        - regime_multiplier: number between 0.90 and 1.10
                        - notes: 1-2 short strings
                """
            },
            {

                "role": "user",
                "content": ""
            }

        ]

    )

    return json.loads(response.output_text)
