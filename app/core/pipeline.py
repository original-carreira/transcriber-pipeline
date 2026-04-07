class Pipeline:

    def __init__(self, services):
        self.services = services

    def run(self, input_file: str, output_dir: str):
        print("\n=== INICIANDO PIPELINE ===\n")

        # 1. Extração de áudio
        audio_path = self.services.audio.extract(input_file)

        # 2. Transcrição
        transcript = self.services.transcription.transcribe(audio_path)

        # 3. Organização
        structured = self.services.formatting.organize(transcript.segments)

        # 4. Exportação
        self.services.export.export(structured, output_dir)

        print("\n=== PIPELINE FINALIZADO ===\n")