from dataclasses import dataclass
from typing import List
from app.models.segment import Segment

@dataclass
class Transcript:
    segments: List[Segment]
    full_text: str