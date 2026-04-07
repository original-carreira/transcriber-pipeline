from app.services.audio_service import AudioService
from app.services.transcription_service import TranscriptionService
from app.services.formatting_service import FormattingService
from app.services.export_service import ExportService

class ServiceContainer:

    def __init__(self):
        self.audio = AudioService()
        self.transcription = TranscriptionService()
        self.formatting = FormattingService()
        self.export = ExportService()