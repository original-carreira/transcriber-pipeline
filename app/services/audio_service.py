from app.utils.path_utils import get_resource_path
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
    def __init__(self):
        
        # ✅ CAMINHO CORRETO PARA .EXE
        self.ffmpeg_path = get_resource_path("ffmpeg/ffmpeg.exe")

        if not Path(self.ffmpeg_path).exists():
            raise FileNotFoundError(
                f"FFmpeg não encontrado em: {self.ffmpeg_path}"
            )

    def extract(self, input_file: str, temp_dir:str = None) -> str:
        # manter método público simples para a pipeline
        return self.extract_audio(input_file, temp_dir)

    def extract_audio(self, input_file: str, temp_dir:str = None) -> str:
        input_path = Path(input_file)

        if not input_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
        
        # fallback
        if not temp_dir:
            temp_dir = "temp"
            
        temp_path = Path(temp_dir)
        temp_path.mkdir(parents=True, exist_ok=True)       
        
        
        output_file = temp_path / f"{input_path.stem}.wav"

        command = [
            self.ffmpeg_path,  # ✅ USAR CAMINHO RESOLVIDO
            "-y",
            "-i", str(input_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output_file)
        ]

        try:
            print("[AudioService] Usando ffmpeg em:", self.ffmpeg_path)
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
                f"Erro ao extrair áudio com ffmpeg:\n{e.stderr.decode(errors='ignore')}"
            )