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
        self.model_size = "base"     # ⚖️ equilíbrio ideal (default)
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

    def _get_config(self, mode: str):
        """
        Define configuração de inferência por modo.

        fast:
            - mais rápido
            - menor qualidade
            - sem contexto entre segmentos

        balanced:
            - melhor coerência
            - ainda viável em CPU
        """

        if mode == "fast":
            return {
                "model": "base",
                "beam_size": 1,
                "vad_filter": True,
                "condition_on_previous_text": False
            }

        # padrão: balanced
        return {
            "model": "base",
            "beam_size": 2,
            "vad_filter": True,
            "condition_on_previous_text": True
        }

    def transcribe(self, audio_path: str, mode: str = "balanced", callback=None) -> Transcript:
        print(f"[TranscriptionService] Iniciando processamento: {audio_path}")
        print(f"[TranscriptionService] Modo: {mode}")

        # 🔧 aplica configuração por modo
        config = self._get_config(mode)

        # 🔄 troca de modelo (se necessário)
        if self.model_size != config["model"]:
            self.model = None
            self.model_size = config["model"]

        # 🔥 Lazy loading (só carrega quando necessário)
        self._load_model()

        """
        CONFIGURAÇÃO DINÂMICA:

        fast:
            - beam_size=1 → máximo desempenho
            - sem contexto → mais rápido

        balanced:
            - beam_size=2 → melhor qualidade
            - com contexto → mais coerência

        comum aos dois:
            - vad_filter=True → acelera removendo silêncio
            - min_silence_duration_ms=500 → evita cortes agressivos
        """

        segments_generator, info = self.model.transcribe(
            audio_path,
            beam_size=config["beam_size"],
            language="pt",
            vad_filter=config["vad_filter"],
            vad_parameters=dict(min_silence_duration_ms=500),
            condition_on_previous_text=config["condition_on_previous_text"]
        )

        print(f"[TranscriptionService] Idioma detectado: {info.language}")

        segments = []

        # 📊 duração total para cálculo de progresso real
        total_duration = info.duration if hasattr(info, "duration") else None

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

            # 📈 progresso real (0 → 1)
            if callback and total_duration:
                progress = whisper_segment.end / total_duration
                progress = min(progress, 1.0)

                callback({
                    "type": "progress",
                    "value": progress
                })

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