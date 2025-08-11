from typing import List, Dict
import math
from .fpl import fetch_boostrap, normalize_players

def project_gw(gameweek: int, risk_tolerance: float = 0.5) -> List[Dict]:
    data = fetch_boostrap()
    players = normalize_players(data)
    out = []
    for player in players:
        ep = max(0.0, player.get("ep_next", 0.0))
        chance = player.get("chance_next")
        availability = (chance / 100.0) if chance is not None else 0.9
        minutes_factor = (0.6 + 0.4 * risk_tolerance) * availability + (0.2 * (1 - risk_tolerance))
        xpts = ep * minutes_factor
        variance = max(0.5, 0.2 + (2.0 * (1 - risk_tolerance)))
        p95 = xpts + 1.64 * math.sqrt(variance)
        out.append({
            "player": {
                "id": player["id"],
                "name": player["name"],
                "team": player["team"],
                "position": player["position"],
                "price": player["price"],
                "club_id": player["club_id"],
            },
            "gw": gameweek,
            "xmins": 90.0 * availability,
            "xpts_mean": round(xpts, 2),
            "xpts_p95": round(p95, 2),
            "variance": round(variance, 3),
            "rationale": {
                "ep_next": round(ep, 2),
                "availability": round(availability, 2),
                "minutes_factor": round(minutes_factor, 2)
            }
        })

    out.sort(key=lambda x: x["xpts_mean"], reverse=True)
    return out

