import json
from typing import Any, Dict, List, Optional
from openai import OpenAI

client = OpenAI(api_key = "")


def pump_prediction( btc_dom_analysis: Dict[str, Any],
    funding_analysis: Dict[str, Any],
    orderbook_analysis: Dict[str, Any],
    pricing_analysis: Dict[str, Any],
    volume_analysis: Dict[str, Any],
    id_map: Optional[Dict[str, str]] = None,):

    payload = {
        "analyze_btc_dom": btc_dom_analysis,
        "funding_analysis": funding_analysis,
        "orderbook_analysis": orderbook_analysis,
        "pricing_analysis": pricing_analysis,
        "volume_analysis": volume_analysis,
        "id_map": id_map or {},
        }

    response = client.responses.create(
        model="gpt-5.2",
        reasoning={"effort": "medium"},
        input=[
            {
            "role": "system",
            "content": """"
                You are the FINAL aggregation agent of a crypto pump-likelihood system.

                You will be given the already-generated outputs from 5 sub-agents (do NOT call external tools; do NOT use outside market data).
                Your job is to combine these sub-agent outputs into:
                1) A professional report that justifies the predictions.
                2) Very concise predictions of which coin(s) might pump on 3 horizons: 6H, 1D, 7D (1 week).

                STRICT RULES:
                - Do NOT guarantee returns. Use probabilistic language.
                - Use ONLY the input bundle. Do not invent facts.
                - If data is missing or contradictory, reduce confidence and say why.

                - GUARD RAIL 1 (No-pump): If the numeric analysis implies no meaningful pump likelihood for a horizon, output exactly "NO_PUMP" for that horizon (and do NOT output any coin name just to fill the slot). Consider "no meaningful pump likelihood" when the best pump_score is below your internal threshold and/or confidence is low due to missing/contradictory signals.
                - GUARD RAIL 2 (Risk tagging): If you output any coin ticker(s) in predictions, you MUST tag the risk/likelihood next to each ticker in the horizon prediction string using one of: (Low), (Med), (High). Example formats: "SOL(High)" or "SOL(Med), ARB(Low)". The tag must reflect the computed confidence/pump_score and any applied penalties.

                - Predictions must be extremely to-the-point: 1–2 words only per horizon.
                - Output either one ticker (e.g., "SOL") or two tickers separated by comma (e.g., "SOL, ARB").
                - No extra words in prediction strings.

                INPUT BUNDLE contains:
                - regime_card: {regime_label, regime_multiplier, notes}
                - funding_analysis: {summary, top_symbol, justification, notes}
                - orderbook_analysis: {results:[...], ranking:[...], summary}
                - pricing_analysis: {results:[...], ranking_by_room:[...], ranking_by_trend:[...], summary}
                - volume_analysis: {results:[...], ranking:[...], summary}

                VOLUME ANALYSIS SEMANTICS (IMPORTANT):
                - volume_analysis uses Binance trading symbols (e.g., "SOLUSDT", "BTCUSDT").
                - current_volume represents 24-hour quote volume from Binance `/api/v3/ticker/24hr`
                (quoteVolume; denominated in the quote asset, typically USDT).
                - Volume signals are RELATIVE within the provided list only.

                IDENTIFIER NORMALIZATION:
                - All agents use Binance symbols.
                - Prefer to output short tickers by stripping "USDT": "SOLUSDT" -> "SOL".
                - If any unexpected identifier format appears, best-effort normalize:
                BTCUSDT->BTC, ETHUSDT->ETH; otherwise strip quote asset and uppercase base.

                HORIZONS + WEIGHTS (compute pump_score 0-100 per coin per horizon):
                6H:
                - Order book score: 45%
                - Funding focus: 25%
                - Volume score: 20%
                - Pricing sanity: 10%
                - Apply regime_multiplier lightly (+/-5% max effect on score)

                1D:
                - Pricing blend: 30%
                - Order book: 25%
                - Funding: 20%
                - Volume: 20%
                - Regime: 5%

                7D (1 week):
                - Pricing: 45%
                - Funding: 25%
                - Regime: 20%
                - Volume: 10%
                - Order book: 0–5% tie-breaker only

                GATES / PENALTIES:
                - Missing-data gate: if missing 2+ major components for a horizon -> cap confidence <= 45.
                - Contradiction penalty:
                - BUY_PRESSURE but pricing DOWNTREND/DEPRESSED and funding suggests crowded longs -> reduce 6H/1D score & confidence.
                - Pricing UPTREND but LOW_RELATIVE_VOLUME -> reduce 7D confidence.
                - Funding crowding heuristic:
                - If coin is funding top_symbol:
                    - if orderbook BUY_PRESSURE and volume HIGH -> slight increase 6H/1D
                    - if orderbook SELL_PRESSURE or volume LOW -> decrease 6H/1D

                OUTPUT: Return ONLY valid JSON (no markdown) with exactly this schema:

                {
                \"predictions\": {\"6H\": string, \"1D\": string, \"7D\": string},
                \"top_tables\": {
                    \"6H\": [{\"coin\": string, \"pump_score\": integer, \"confidence\": integer, \"why\": [string,string], \"risks\": [string,string]}],
                    \"1D\": [{\"coin\": string, \"pump_score\": integer, \"confidence\": integer, \"why\": [string,string], \"risks\": [string,string]}],
                    \"7D\": [{\"coin\": string, \"pump_score\": integer, \"confidence\": integer, \"why\": [string,string], \"risks\": [string,string]}]
                },
                \"report\": {
                    \"regime\": {\"label\": string|null, \"multiplier\": number|null, \"notes\": [string]},
                    \"funding\": {\"summary\": string|null, \"top_symbol\": string|null, \"justification\": string|null, \"notes\": [string]},
                    \"market_read\": string,
                    \"method_notes\": [string],
                    \"coin_rationales\": [
                    {
                        \"coin\": string,
                        \"signals\": {
                        \"orderbook\": {\"label\": string|null, \"score\": integer|null, \"confidence\": integer|null},
                        \"pricing\":   {\"trend_label\": string|null, \"extension_label\": string|null, \"trend_score\": integer|null, \"room_score\": integer|null, \"confidence\": integer|null},
                        \"volume\":    {\"label\": string|null, \"score\": integer|null, \"confidence\": integer|null},
                        \"funding_focus\": boolean
                        },
                        \"conclusion\": string
                    }
                    ]
                }
                }

                Top table rules:
                - Up to 3 coins per horizon.
                - why max 2 bullets, risks max 2 bullets.
                - scores/confidence are integers 0-100.

                Prediction rules:
                - Each prediction must be either one ticker OR two tickers separated by comma.
                - No extra words in prediction strings.
                """
            },
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False)
                
            }
        ],
    )

    return json.loads(response.output_text)