from app.models.structured_content import StructuredContent
from app.models.segment import Segment
from typing import List

class FormattingService:

    def organize(self, segments: List[Segment]) -> StructuredContent:
        print("[FormattingService] Organizando conteúdo (mock)...")

        sections = [
            {
                "title": "Seção 1",
                "content": " ".join([s.text for s in segments])
            }
        ]

        full_text = sections[0]["content"]

        return StructuredContent(
            sections=sections,
            full_text=full_text
        )