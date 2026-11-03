from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Card:
    reps: int = 0
    interval: int = 0
    ease: float = 2.5
