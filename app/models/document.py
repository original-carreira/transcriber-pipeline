from dataclasses import dataclass
from typing import List

@dataclass
class Paragraph:
    text: str

@dataclass
class Document:
    paragraphs: List[Paragraph]
    title: str = "Transcrição"