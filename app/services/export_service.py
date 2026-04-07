import os
from app.models.structured_content import StructuredContent

class ExportService:

    def export(self, data: StructuredContent, output_dir: str):
        print("[ExportService] Exportando conteúdo (mock)...")

        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, "output.txt")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(data.full_text)

        print(f"[ExportService] Arquivo gerado em: {output_file}")