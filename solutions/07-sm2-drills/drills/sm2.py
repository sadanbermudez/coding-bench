from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Card:
    reps: int = 0
    interval: int = 0
    ease: float = 2.5


def review(card, quality):
    if not isinstance(quality, int) or isinstance(quality, bool) or not 0 <= quality <= 5:
        raise ValueError(quality)
    if quality < 3:
        return Card(0, 1, card.ease)
    iv = 1 if card.reps == 0 else 6 if card.reps == 1 else round(card.interval * card.ease)
    q = 5 - quality
    ease = max(1.3, card.ease + (0.1 - q * (0.08 + q * 0.02)))
    return Card(card.reps + 1, iv, ease)


def due(card, last_review):
    return last_review + timedelta(days=card.interval)
