import os
from docx import Document as DocxDocument
from app.models.document import Document
from datetime import datetime


class ExportServiceMock:

    def export(self, data: Document, output_dir: str):
        print("[ExportService] Exportando conteúdo...")

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"output_{timestamp}.txt")

        with open(output_file, "w", encoding="utf-8") as f:
            for paragraph in data.paragraphs:
                f.write(paragraph.text + "\n\n")

        print(f"[ExportService] Arquivo gerado em: {output_file}")


# app/services/export_service.py
class ExportService:

    def export(self, data: Document, output_dir: str, format: str = "txt"):
        print("[ExportService] Exportando conteúdo...")

        os.makedirs(output_dir, exist_ok=True)

        if format == "txt":
            self._export_txt(data, output_dir)

        elif format == "docx":
            self._export_docx(data, output_dir)

        else:
            raise ValueError(f"Formato não suportado: {format}")

    # =========================
    # TXT
    # =========================
    def _export_txt(self, data: Document, output_dir: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"output_{timestamp}.txt")

        with open(output_file, "w", encoding="utf-8") as f:
            for paragraph in data.paragraphs:
                f.write(paragraph.text + "\n\n")

        print(f"[ExportService] TXT gerado em: {output_file}")

    # =========================
    # DOCX
    # =========================
    def _export_docx(self, data: Document, output_dir: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"transcricao_{timestamp}.docx")

        doc = DocxDocument()

        # Título (garantido)
        title = getattr(data, "title", "Transcrição")
        doc.add_heading(title, level=1)

        # Parágrafos
        for paragraph in data.paragraphs:
            p = doc.add_paragraph(paragraph.text)
            p.paragraph_format.space_after = 12

        doc.save(output_file)

        print(f"[ExportService] DOCX gerado em: {output_file}")