class Pipeline:
    def __init__(self, services):
        """
        Pipeline principal.

        Recebe um ServiceContainer contendo:
        - audio
        - transcription
        - formatting
        - export
        """
        self.services = services

    def run(
        self,
        input_file: str,
        output_dir: str,
        format: str = "txt",
        callback=None
    ):
        """
        Executa o pipeline completo de forma sequencial.

        :param input_file: caminho do arquivo de entrada
        :param output_dir: diretório de saída
        :param format: formato de exportação (txt | docx)
        :param callback: função opcional para logs (callback(message: str))
        """

        def log(message: str):
            """Encapsula o callback para evitar repetição"""
            if callback:
                callback(message)

        try:
            # ----------------------------------------
            # 1. EXTRAÇÃO DE ÁUDIO
            # ----------------------------------------
            log("Extraindo áudio...")
            audio_path = self.services.audio.extract(input_file)

            # ----------------------------------------
            # 2. TRANSCRIÇÃO
            # ----------------------------------------
            log("Transcrevendo áudio...")
            transcript = self.services.transcription.transcribe(audio_path)

            # ----------------------------------------
            # 3. ORGANIZAÇÃO DO TEXTO
            # CORREÇÃO APLICADA AQUI:
            # Agora usamos transcript.segments
            # ----------------------------------------
            log("Organizando texto...")
            structured = self.services.formatting.organize(
                transcript.segments
            )

            # ----------------------------------------
            # 4. EXPORTAÇÃO
            # ----------------------------------------
            log(f"Exportando arquivo ({format.upper()})...")
            output_path = self.services.export.export(
                structured,
                output_dir=output_dir,
                format=format
            )

            # ----------------------------------------
            # FINALIZAÇÃO
            # ----------------------------------------
            log(f"Concluído: {output_path}")

            return output_path

        except Exception as e:
            # Log de erro sem alterar fluxo arquitetural
            log(f"Erro no pipeline: {str(e)}")
            raise