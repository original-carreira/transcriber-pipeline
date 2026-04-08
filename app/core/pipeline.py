from app.utils.app_paths import get_output_dir, get_temp_dir

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
        callback=None,
        mode: str = "balanced"
    ):
        """
        Executa o pipeline completo de forma sequencial.

        Responsabilidades:
        - Orquestrar os serviços
        - Repassar parâmetros (mode, callback)
        - Não contém lógica de negócio

        :param input_file: caminho do arquivo de entrada
        :param output_dir: diretório de saída
        :param format: formato de exportação (txt | docx | json | srt)
        :param callback: função opcional para logs (callback(message: str))
        :param mode: modo de transcrição (fast | balanced)
        """

        def log(message: str):
            """
            Encapsula o callback para evitar repetição.
            Mantém compatibilidade com a UI atual.
            """
            if callback:
                callback(message)

        try:
            # ---------------------------------------
            # RESOLUÇÃO DE DIRETÓRIOS
            # ---------------------------------------            
            if not output_dir:
                output_dir = get_output_dir()
                
            temp_dir = get_temp_dir() # reservado para o futuro
            # ----------------------------------------
            # 1. EXTRAÇÃO DE ÁUDIO
            # ----------------------------------------
            log("Extraindo áudio...")
            audio_path = self.services.audio.extract(input_file)

            # ----------------------------------------
            # 2. TRANSCRIÇÃO (COM SUPORTE A MODE)
            # ----------------------------------------
            log("Transcrevendo áudio...")

            # IMPORTANTE:
            # - Apenas repasse do parâmetro "mode"
            # - Pipeline não decide comportamento interno
            transcript = self.services.transcription.transcribe(
                audio_path,
                mode=mode,
                callback=callback
            )

            # ----------------------------------------
            # 3. ORGANIZAÇÃO DO TEXTO
            # ----------------------------------------
            log("Organizando texto...")

            # Mantém uso de segments conforme correção anterior
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
                format=format, 
                segments=transcript.segments
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