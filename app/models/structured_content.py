from dataclasses import dataclass
from typing import List, Dict

@dataclass
class StructuredContent:
    sections: List[Dict]
    full_text: str