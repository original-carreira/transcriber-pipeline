import os

class AudioService:

    def extract(self, input_path: str) -> str:
        print("[AudioService] Extraindo áudio (mock)...")

        fake_audio_path = os.path.splitext(input_path)[0] + ".wav"

        print(f"[AudioService] Áudio gerado: {fake_audio_path}")
        return fake_audio_path