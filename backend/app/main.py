from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .schemas import ProjectionsResponse, OptimizeRequest, OptimizeResponse, ChipAdvice
from .services.projections import project_gw
from .services.optimizer import optimize_xi
from .services.chips import chip_suggestion

app = FastAPI(title="FPL Assistant MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/projections/{gameweek}", response_model=ProjectionsResponse)
def projections(gameweek: int, risk: float = 0.5):
    projections = project_gw(gameweek=gameweek, risk_tolerance=risk)
    return {"gameweek": gameweek, "projections": projections}

@app.post("/optimize/xi", response_model=OptimizeResponse)
def optimize(request: OptimizeRequest):
    projs = project_gw(gameweek=request.gw, risk_tolerance=request.risk_tolerance)
    xi, bench, cap_id, total_cost, exp_pts = optimize_xi(projections=projs, budget=request.budget, formation=request.formation,
                     lock_player_ids=request.lock_player_ids, exclude_player_ids=request.exclude_player_ids)

    explanation = (
        f"Optimized {request.formation} under £{request.budget}m. "
        f"Captain chosen to maximize expected points given projections."
    )

    def to_role(p):
        role = p["player"]["position"]
        if p["player"]["id"] == cap_id:
            role = "C"
        return {"player": p["player"], "role": role}

    advice = chip_suggestion(gameweek=request.gw, xi=xi)

    return {
        "gameweek": request.gw,
        "total_cost": round(total_cost, 1),
        "expected_points": round(exp_pts, 1),
        "xi": [to_role(p) for p in xi],
        "bench": [p["player"] for p in bench],
        "captain_id": cap_id,
        "explanation": explanation
    }

@app.get("/chips/suggest", response_model=ChipAdvice)
def chips(gameweek: int):
    projs = project_gw(gameweek=gameweek)
    xi, _, _, _, _ = optimize_xi(projections=projs, budget=100.0, formation="3-4-3")
    advice = chip_suggestion(gameweek=gameweek, xi=xi)
    return advice
