from typing import List, Dict, Tuple
import pulp

POS_ORDER = ["GK", "DEF", "MID", "FWD"]

FORMATIONS = {
    "3-4-3": {"GK": (1, 2), "DEF": (3, 5), "MID": (4, 5), "FWD": (3, 3)},
    "3-5-2": {"GK": (1, 2), "DEF": (3, 5), "MID": (5, 5), "FWD": (2, 3)},
    "4-4-2": {"GK": (1, 2), "DEF": (4, 5), "MID": (4, 5), "FWD": (2, 3)},
}

def optimize_xi(projections: List[Dict], budget: float = 100.0, formation: str = "3-4-3",
                lock_player_ids: List[int] = None, exclude_player_ids: List[int] = None) -> Tuple[List[Dict], List[Dict], int, float, float]:
    lock_player_ids = lock_player_ids or []
    exclude_player_ids = exclude_player_ids or []
    limits = FORMATIONS.get(formation, FORMATIONS["3-4-3"])

    probability = pulp.LpProblem("BestXI", sense=pulp.LpMaximize)
    ids = [p["player"]["id"] for p in projections]
    x = pulp.LpVariable.dicts("sel", ids, lowBound=0, upBound=1, cat="Binary")
    c = pulp.LpVariable.dicts("cap", ids, lowBound=0, upBound=1, cat="Binary")

    points = {p["player"]["id"]: p["xpts_mean"] for p in projections}
    price = {p["player"]["id"]: p["player"]["price"] for p in projections}
    position = {p["player"]["id"]: p["player"]["position"] for p in projections}
    club = {p["player"]["id"]: p["player"]["club_id"] for p in projections}

    probability += pulp.lpSum([points[i] * x[i] for i in ids]) + pulp.lpSum([points[i] * c[i] for i in ids])

    probability += pulp.lpSum([x[i] for i in ids]) == 11

    probability += pulp.lpSum([c[i] for i in ids]) == 1
    for i in ids:
        probability += c[i] <= x[i]

    for ptype in POS_ORDER:
        lo, hi = limits[ptype]
        probability += pulp.lpSum([x[i] for i in ids if position[i] == ptype]) >= lo
        probability += pulp.lpSum([x[i] for i in ids if position[i] == ptype]) <= hi

    probability += pulp.lpSum([price[i] * x[i] for i in ids]) <= budget

    clubs = set(club.values())
    for cl in clubs:
        probability += pulp.lpSum([x[i] for i in ids if club[i] == cl]) <= 3

    for i in lock_player_ids:
        if i in ids:
            probability += x[i] == 1
    for i in exclude_player_ids:
        if i in ids:
            probability += x[i] == 0

    probability.solve(pulp.PULP_CBC_CMD(msg=False))

    sel_ids = [i for i in ids if pulp.value(x[i]) > 0.5]
    cap_id = next((i for i in ids if pulp.value(c[i]) > 0.5), sel_ids[0])

    xi = [p for p in projections if p["player"]["id"] in sel_ids]
    bench = sorted([p for p in projections if p["player"]["id"] not in sel_ids], key=lambda r: r["player"]["price"])[:4]

    total_cost = sum(price[i] for i in sel_ids)
    exp_pts = sum([points[i] for i in sel_ids]) + points.get(cap_id, 0)
    return xi, bench, cap_id, total_cost, exp_pts

