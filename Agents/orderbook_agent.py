import json
from openai import OpenAI

client = OpenAI(api_key = "")

def analyze_orderbook (orderbooks: list[dict]) -> dict:
    payload = {"orderbooks": orderbooks}

    response = client.responses.create(
        model="gpt-5.2",
        reasoning={"effort": "medium"},
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are an Order Book Microstructure Analyst for crypto markets.\n\n"
                            "You will receive order book summary data for multiple symbols.\n"
                            "Each item has: symbol, mid_level, bid_qty_total, ask_qty_total.\n\n"
                            "Task:\n"
                            "1) For each symbol, compute and interpret near-price liquidity balance.\n"
                            "2) Produce a conservative, probabilistic upside-pressure signal per symbol.\n"
                            "3) Rank symbols by short-term upside pressure likelihood.\n"
                            "4) Note key risks (snapshot-only, spoofing risk, invalid data).\n\n"
                            "Rules:\n"
                            "- imbalance = (bid_qty_total - ask_qty_total) / (bid_qty_total + ask_qty_total) if denom>0 else 0\n"
                            "- BUY_PRESSURE if imbalance >= +0.10, SELL_PRESSURE if <= -0.10, else BALANCED\n"
                            "- Use ratios/imbalance; do not rely on absolute quantities.\n"
                            "- Do NOT guarantee returns.\n\n"
                            "Return ONLY valid JSON with this schema:\n"
                            "{\n"
                            '  "results": [\n'
                            "    {\n"
                            '      "symbol": string,\n'
                            '      "metrics": {\n'
                            '        "mid_level": number,\n'
                            '        "bid_qty_total": number,\n'
                            '        "ask_qty_total": number,\n'
                            '        "imbalance": number,\n'
                            '        "bid_ask_ratio": number\n'
                            "      },\n"
                            '      "signal": {\n'
                            '        "label": "BUY_PRESSURE" | "SELL_PRESSURE" | "BALANCED",\n'
                            '        "score": integer,\n'
                            '        "confidence": integer,\n'
                            '        "time_horizon_hint": "VERY_SHORT"\n'
                            "      },\n"
                            '      "reasons": [string, string],\n'
                            '      "watchouts": [string]\n'
                            "    }\n"
                            "  ],\n"
                            '  "ranking": [string, string, string],\n'
                            '  "summary": string\n'
                            "}\n"
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": json.dumps(payload, ensure_ascii=False)}
                ],
            },
        ],
    )

    return json.loads(response.output_text)
