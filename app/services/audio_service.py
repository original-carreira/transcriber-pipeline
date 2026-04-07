from pathlib import Path
import os
import subprocess


class AudioServiceMock:

    def extract(self, input_path: str) -> str:
        print("[AudioService] Extraindo áudio (mock)...")

        fake_audio_path = os.path.splitext(input_path)[0] + ".wav"

        print(f"[AudioService] Áudio gerado: {fake_audio_path}")
        return fake_audio_path
    
    

# services/audio_service.py
class AudioService:
    def __init__(self, output_dir: str = "temp"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, input_file: str) -> str:
        # manter método público simples para a pipeline, delegando a lógica real para outro método
        return self.extract_audio(input_file)
    
    def extract_audio(self, input_file: str) -> str:
        """
        Extrai áudio de um arquivo de vídeo e salva como WAV.

        Args:
            input_file (str): Caminho do arquivo de vídeo

        Returns:
            str: Caminho do arquivo WAV gerado
        """

        input_path = Path(input_file)

        if not input_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")

        output_file = self.output_dir / f"{input_path.stem}.wav"

        command = [
            "ffmpeg",
            "-y",  # sobrescrever sem perguntar
            "-i", str(input_path),
            "-vn",  # remove vídeo
            "-acodec", "pcm_s16le",  # codec WAV padrão
            "-ar", "16000",  # sample rate ideal para Whisper
            "-ac", "1",  # mono (reduz custo e melhora transcrição)
            str(output_file)
        ]

        try:
            print("[AudioService] Extraindo áudio com ffmpeg...")

            subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            print(f"[AudioService] Áudio gerado: {output_file}")

            return str(output_file)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Erro ao extrair áudio com ffmpeg:\n{e.stderr.decode()}"
            )