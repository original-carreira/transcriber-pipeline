from faster_whisper import WhisperModel

from app.models.transcript import Transcript
from app.models.segment import Segment

class TranscriptionServiceMock:

    def transcribe(self, audio_path: str) -> Transcript:
        print("[TranscriptionService] Transcrevendo áudio (mock)...")

        segments = [
            Segment(0.0, 5.0, "Olá, este é um teste de transcrição."),
            Segment(5.0, 10.0, "Estamos simulando um pipeline de processamento."),
        ]

        full_text = " ".join([s.text for s in segments])

        return Transcript(segments=segments, full_text=full_text)

class TranscriptionService:

    def __init__(self, model_size: str = "tiny", device: str = "cpu"):
        """
        model_size: tiny, base, small, medium, large
        device: "cpu" ou "cuda"
        """
        print(f"[TranscriptionService] Carregando modelo: {model_size} ({device})")
        self.model = WhisperModel(model_size, device=device)

    def transcribe(self, audio_path: str) -> Transcript:
        print("[TranscriptionService] Transcrevendo áudio...")

        segments_generator, info = self.model.transcribe(audio_path, language="pt", beam_size=1)

        segments = []

        for segment in segments_generator:
            segments.append(
                Segment(
                    start=segment.start,
                    end=segment.end,
                    text=segment.text.strip()
                )
            )

        full_text = " ".join([s.text for s in segments])

        print(f"[TranscriptionService] Idioma detectado: {info.language}")

        return Transcript(
            segments=segments,
            full_text=full_text
        )