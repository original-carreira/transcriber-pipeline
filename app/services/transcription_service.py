from faster_whisper import WhisperModel

from app.models.transcript import Transcript
from app.models.segment import Segment


class TranscriptionService:
    def __init__(self):
        """
        PERFIL EQUILIBRADO (CPU-friendly)

        Decisões:
        - modelo: base → muito mais rápido que medium
        - compute_type: int8 → reduz uso de RAM
        - NÃO carregar modelo aqui (lazy loading)
        """

        self.model = None
        self.model_size = "base"     # ⚖️ equilíbrio ideal
        self.device = "cpu"
        self.compute_type = "int8"

    def _load_model(self):
        """
        Carregamento sob demanda (evita travar a UI na inicialização)
        """
        if self.model is None:
            print(f"[TranscriptionService] Carregando modelo: {self.model_size}")

            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )

    def transcribe(self, audio_path: str) -> Transcript:
        print(f"[TranscriptionService] Iniciando processamento: {audio_path}")

        # 🔥 Lazy loading (só carrega quando necessário)
        self._load_model()

        """
        CONFIGURAÇÃO EQUILIBRADA:

        beam_size=2
            → melhora qualidade sem custo alto

        vad_filter=True
            → remove silêncios e acelera processamento

        min_silence_duration_ms=500
            → evita cortes agressivos (mantém frases)

        condition_on_previous_text=True
            → mantém contexto entre segmentos
        """

        segments_generator, info = self.model.transcribe(
            audio_path,
            beam_size=2,  # ⚖️ equilíbrio entre qualidade e velocidade
            language="pt",
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            condition_on_previous_text=True
        )

        print(f"[TranscriptionService] Idioma detectado: {info.language}")

        segments = []

        for whisper_segment in segments_generator:
            clean_text = whisper_segment.text.strip()

            # ignora segmentos vazios
            if not clean_text:
                continue

            segments.append(
                Segment(
                    start=whisper_segment.start,
                    end=whisper_segment.end,
                    text=clean_text
                )
            )

            # log de progresso por tempo processado
            print(f"[TranscriptionService] {whisper_segment.end:.1f}s processados")

        # segurança: evitar retorno inválido
        if not segments:
            print("[WARNING] Nenhum segmento foi gerado")

        full_text = " ".join([s.text for s in segments])

        return Transcript(
            segments=segments,
            full_text=full_text
        )