import json
from openai import OpenAI

client = OpenAI(api_key = "")

def analyze_fundrate (fundrate_details):

    fundrate_text = json.dumps(fundrate_details)

    response = client.responses.create(
        model = "gpt-5.2",
        reasoning = {"effort": "medium"},
        input = [
            {
                "role": "system",
                "content": (
                    "You are a crypto market analyst.\n"
                    "Given funding rate data for multiple symbols:\n"
                    "- Summarize what the funding rates suggest about positioning/imbalance\n"
                    "- Identify which symbol looks most likely to have a short-term move\n"
                    "- Provide a brief justification\n"
                    "Important: Do not guarantee returns; treat this as probabilistic analysis.\n\n"
                    "Return ONLY valid JSON with keys:\n"
                    "- summary (string)\n"
                    "- top_symbol (string)\n"
                    "- justification (string)\n"
                    "- notes (array of strings)\n"
                ),
            },
            {
                "role": "user",
                "content": fundrate_text
            }
        ]

    )

    return json.loads(response.output_text)