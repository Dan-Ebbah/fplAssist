import requests
from typing import List, Dict, Any

FPL_BASE_URL = "https://fantasy.premierleague.com/bootstrap-static/"

POSITION_MAP = {
    1: "GK",
    2: "DEF",
    3: "MID",
    4: "FWD"
}

class FPLError(RuntimeError):
    """Custom exception for FPL service errors."""
    pass

def fetch_boostrap() -> Dict[str, Any]:
    res = requests.get(FPL_BASE_URL, timeout=20)
    if not res.ok:
        raise FPLError(f"Failed to fetch FPL bootstrap data: {res.status_code} {res.reason}")
    return res.json()


def normalize_players(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    teams = {t["id"]: t["name"] for t in data["teams"]}
    out = []
    for player in data["elements"]:
        normalized_player = {
            "id": player["id"],
            "name": f"{player['first_name']} {player['second_name']}",
            "team": teams[player["team"]],
            "position": POSITION_MAP.get(player["element_type"], "UNK"),
            "price": player["now_cost"] / 10.0,  # Convert from tenths of a million to millions
            "club_id": player["team"],
            "ep_next": float(player.get("ep_next", 0.0) or 0.0),
            "chance_next": player.get("chance_of_playing_next_round"),
        }
        out.append(normalized_player)

    return out


