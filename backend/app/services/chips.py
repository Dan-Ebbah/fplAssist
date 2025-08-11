from typing import List, Dict

def chip_suggestion(gameweek: int, xi: List[Dict]) -> Dict:
    if not xi:
        return {"gameweek": gameweek, "recommendation": None, "confidence": 0.0, "reasons": ["No XI computed yet."]}

    sorted_xi = sorted(xi, key=lambda p: p["xpts_mean"], reverse=True)
    top = sorted_xi[0]
    median = sorted_xi[len(sorted_xi) // 2]
    delta = top["xpts_mean"] - median["xpts_mean"]

    if delta >= 2.5 and top["player"]["position"] in ["MID", "FWD"]:
        return {
            "gameweek": gameweek,
            "recommendation": "TRIPLE_CAPTAIN",
            "confidence": min(0.9, 0.5 + delta / 5.0),
            "reasons": [
                f"Top captain {top['player']['name']} projects {top['xpts_mean']:.1f} which is {delta:.1f} above median in your XI.",
                "Heuristic v1 – refine with double/blank detection later."
            ]
        }

    return {"gameweek": gameweek, "recommendation": None, "confidence": 0.3, "reasons": ["No strong chip edge detected."]}