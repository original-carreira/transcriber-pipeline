from app.models.transcript import Transcript
from app.models.segment import Segment

class TranscriptionService:

    def transcribe(self, audio_path: str) -> Transcript:
        print("[TranscriptionService] Transcrevendo áudio (mock)...")

        segments = [
            Segment(0.0, 5.0, "Olá, este é um teste de transcrição."),
            Segment(5.0, 10.0, "Estamos simulando um pipeline de processamento."),
        ]

        full_text = " ".join([s.text for s in segments])

        return Transcript(segments=segments, full_text=full_text)