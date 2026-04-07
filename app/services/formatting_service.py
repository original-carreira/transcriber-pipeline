from app.models.segment import Segment
from app.models.document import Document, Paragraph
from typing import List
import re

class FormattingServiceMock:

    def organize(self, segments: List[Segment]) -> Document:
        print("[FormattingService] Organizando conteúdo (mock)...")

        sections = [
            {
                "title": "Seção 1",
                "content": " ".join([s.text for s in segments])
            }
        ]

        full_text = sections[0]["content"]

        return Document(
            sections=sections,
            full_text=full_text
        )
        
class FormattingService:
    def __init__(self):
        pass

    def organize(self, segments: List[Segment]) -> Document:
        """
        Pipeline principal de formatação
        """
        cleaned = [self._normalize_text(s.text) for s in segments]

        grouped = self._group_segments(segments, cleaned)

        paragraphs = self._build_paragraphs(grouped)

        return Document(paragraphs=paragraphs)

    # ----------------------------
    # 1. Normalização
    # ----------------------------
    def _normalize_text(self, text: str) -> str:
        text = text.strip()

        # remover espaços duplicados
        text = re.sub(r"\s+", " ", text)

        # capitalizar início
        if text:
            text = text[0].upper() + text[1:]

        return text

    # ----------------------------
    # 2. Agrupamento
    # ----------------------------
    def _group_segments(self, segments: List[Segment], texts: List[str]):
        grouped = []

        buffer = []
        last_end = None

        for seg, text in zip(segments, texts):
            if not text:
                continue

            pause = 0
            if last_end is not None:
                pause = seg.start - last_end

            # critérios de quebra
            if (
                pause > 1.5 or                # pausa longa
                len(" ".join(buffer)) > 200   # bloco muito grande
            ):
                grouped.append(" ".join(buffer))
                buffer = []

            buffer.append(text)
            last_end = seg.end

        if buffer:
            grouped.append(" ".join(buffer))

        return grouped

    # ----------------------------
    # 3. Parágrafos
    # ----------------------------
    def _build_paragraphs(self, blocks: List[str]) -> List[Paragraph]:
        paragraphs = []

        for block in blocks:
            text = self._improve_punctuation(block)
            paragraphs.append(Paragraph(text=text))

        return paragraphs

    # ----------------------------
    # 4. Pontuação básica
    # ----------------------------
    def _improve_punctuation(self, text: str) -> str:
        text = text.strip()

        # garantir ponto final
        if text and text[-1] not in ".!?":
            text += "."

        # corrigir espaços antes de pontuação
        text = re.sub(r"\s+([.,!?])", r"\1", text)

        return text