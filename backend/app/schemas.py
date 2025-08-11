from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Player(BaseModel):
    id: str
    name: str
    team: str
    position: str
    price: float
    club_id: int

class PlayerProjection(BaseModel):
    player: Player
    gw: int
    xmins: float = Field(description="Expected minutes")
    xpts_mean: float
    xpts_p95: float
    variance: float
    rationale: Dict[str, float]

class ProjectionsResponse(BaseModel):
    gw: int
    projections: List[PlayerProjection]

class OptimizeRequest(BaseModel):
    gw: int
    budget: float = 100.0
    formation: Optional[str] = "3-4-3"
    lock_player_ids: List[int] = []
    exclude_player_ids: List[int] = []
    risk_tolerance: float = 0.5

class XIPlayer(BaseModel):
    player: Player
    role: str

class OptimizeResponse(BaseModel):
    gw: int
    total_cost: float
    expected_points: float
    xi: List[XIPlayer]
    bench: List[Player]
    captain_id: int
    explanation: str

class ChipAdvice(BaseModel):
    gw: int
    recommendation: Optional[str]
    confidence: float
    reasons: List[str]